from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from fack.models import Question, Topic, QuestionScore

# verify if django-contrib-comments is installed
has_comment = False
if 'django_comments' in settings.INSTALLED_APPS:
    from django_comments.models import Comment
    has_comment = True


class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'site', 'sort_order', 'updated_on', 'updated_by']
    list_editable = ['sort_order']
    list_per_page = 40
    raw_id_fields = ['created_by', 'updated_by']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

    def save_model(self, request, obj, form, change):
        if not change and obj.site is None:
            obj.site = Site.objects.get_current()

        super(TopicAdmin, self).save_model(request, obj, form, change)


class TopicAdminForm(forms.ModelForm):
    """
    http://stackoverflow.com/questions/5414853/customize-select-in-django-admin
    """
    def __init__(self, *args, **kwargs):
        super(TopicAdminForm, self).__init__(*args, **kwargs)
        temp = {}
        for topic in self.fields['topic'].queryset.order_by('site'):
            if not topic.site.name in temp:
                temp[topic.site.name] = []
            temp[topic.site.name].append((topic.id, topic.name))
        choices = [[k, v] for k, v in temp.items()]
        self.fields['topic'].choices = choices


class QuestionAdmin(admin.ModelAdmin):
    form = TopicAdminForm
    list_display = ['text', 'topic', 'site', 'sort_order', 'created_by', 'created_on',
                    'updated_by', 'updated_on', 'status', 'useful']
    list_editable = ['sort_order', 'status']
    raw_id_fields = ['created_by', 'updated_by']
    search_fields = ['text', 'answer']
    list_filter = ('topic', 'topic__site', 'status', )
    list_per_page = 40

    readonly_fields = ['useful']

    if has_comment:
        list_display.append('num_comments')
        readonly_fields.append('num_comments')

    def useful(self, obj):
        """
        Calculate the percentage of positive scores.  A positive score is indicated by 1.
        """
        total = self._get_scores(obj).count()

        if total != 0:
            yes = self._get_scores(obj).filter(score=1).count()
            percentage = (float(yes) / float(total)) * 100
            return "{:.2f} % ({})".format(percentage, total)

        # No scores yet
        return "NA"

    def num_comments(self, obj):
        """
        The number of comments for a Question.
        """
        return self._get_comments(obj).count()

    def _get_scores(self, obj):
        """
        Fetch all the QuestionScores for a Question and add them as a property, avoids useless queries to the database.
        """
        if not hasattr(obj, '_scores'):
            obj._scores = QuestionScore.objects.filter(question=obj)

        return obj._scores

    def _get_comments(self, obj):
        """
        Fetch all the comments for a Question and add them as a property, avoids useless queries to the database.
        """
        if not has_comment:
            obj._comments = None
        elif not hasattr(obj, '_comments'):
            content_type = ContentType.objects.get_for_model(obj)
            obj._comments = Comment.objects.filter(content_type=content_type, object_pk=obj.pk)

        return obj._comments

    def save_model(self, request, obj, form, change):
        """
        Update created_by and updated_by fields.

        The model layer updates the date fields, but has no access to the user.
        """
        # If the object is new, update the created_by field.
        if not change:
            obj.created_by = request.user

        # Either way, update the updated_by field.
        obj.updated_by = request.user

        # Let the superclass do the final saving.
        super(QuestionAdmin, self).save_model(request, obj, form, change)

    def site(self, obj):
        return '{}'.format(obj.topic.site.name)


admin.site.register(Question, QuestionAdmin)
admin.site.register(Topic, TopicAdmin)

