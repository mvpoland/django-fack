from __future__ import absolute_import

from django.contrib import admin
from django.contrib.sites.models import Site

from .models import Question, Topic
            

class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'site']
    prepopulated_fields = {'slug':('name',)}
    
    def save_model(self, request, obj, form, change):
        if not change and obj.site is None:
            obj.site = Site.objects.get_current()

        super(TopicAdmin, self).save_model(request, obj, form, change)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'site', 'sort_order', 'created_by', 'created_on',
                    'updated_by', 'updated_on', 'status']
    list_editable = ['sort_order', 'status']
    raw_id_fields = ['created_by', 'updated_by']

    def save_model(self, request, obj, form, change): 
        '''
        Update created_by and updated_by fields.
        
        The model layer updates the date fields, but has no access to the user.
        '''
        # If the object is new, update the created_by field.
        if not change:
            obj.created_by = request.user
        
        # Either way, update the updated_by field.
        obj.updated_by = request.user

        # Let the superclass do the final saving.
        super(QuestionAdmin, self).save_model(request, obj, form, change)

    def site(self, obj):
        return '%s' % (obj.topic.site.name)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Topic, TopicAdmin)
