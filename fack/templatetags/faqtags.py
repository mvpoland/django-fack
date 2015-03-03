from __future__ import absolute_import

from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from ..models import Question, Topic

# verify if django-contrib-comments is installed
has_comment = False
if 'django_comments' in settings.INSTALLED_APPS:
    from django_comments.models import Comment
    has_comment = True

register = template.Library()


class FaqListNode(template.Node):
    def __init__(self, num, varname, topic=None):
        self.num = template.Variable(num)
        self.topic = template.Variable(topic) if topic else None
        self.varname = varname

    def render(self, context):
        try:
            num = self.num.resolve(context)
            topic = self.topic.resolve(context) if self.topic else None
        except template.VariableDoesNotExist:
            return ''

        if isinstance(topic, Topic):
            qs = Question.objects.filter(topic=topic)
        elif topic is not None:
            qs = Question.objects.filter(topic__slug=topic)
        else:
            qs = Question.objects.all()

        context[self.varname] = qs.filter(status=Question.ACTIVE)[:num]
        return ''

@register.tag
def faqs_for_topic(parser, token):
    """
    Returns a list of 'count' faq's that belong to the given topic
    the supplied topic argument must be in the slug format 'topic-name'

    Example usage::

        {% faqs_for_topic 5 "my-slug" as faqs %}
    """

    args = token.split_contents()
    if len(args) != 5:
        raise template.TemplateSyntaxError("%s takes exactly four arguments" % args[0])
    if args[3] != 'as':
        raise template.TemplateSyntaxError("third argument to the %s tag must be 'as'" % args[0])

    return FaqListNode(num=args[1], topic=args[2], varname=args[4])


@register.tag
def faq_list(parser, token):
    """
    returns a generic list of 'count' faq's to display in a list
    ordered by the faq sort order.

    Example usage::

        {% faq_list 15 as faqs %}
    """
    args = token.split_contents()
    if len(args) != 4:
        raise template.TemplateSyntaxError("%s takes exactly three arguments" % args[0])
    if args[2] != 'as':
        raise template.TemplateSyntaxError("second argument to the %s tag must be 'as'" % args[0])

    return FaqListNode(num=args[1], varname=args[3])

class TopicListNode(template.Node):
    def __init__(self, varname):
        self.varname = varname

    def render(self, context):
        context[self.varname] = Topic.objects.all()
        return ''

@register.tag
def faq_topic_list(parser, token):
    """
    Returns a list of all FAQ Topics.

    Example usage::
        {% faq_topic_list as topic_list %}
    """
    args = token.split_contents()
    if len(args) != 3:
        raise template.TemplateSyntaxError("%s takes exactly two arguments" % args[0])
    if args[1] != 'as':
        raise template.TemplateSyntaxError("second argument to the %s tag must be 'as'" % args[0])

    return TopicListNode(varname=args[2])


@register.inclusion_tag('admin/fack/question/comments.html')
def display_comments(obj):
    """
    Custom tag to fetch a list of comments for an object.

    The call to `select_related` is performance boost.  In Django 1.5 you can use `prefetch_related` to narrow it down
    to certain models.

    https://docs.djangoproject.com/en/1.3/ref/models/querysets/#django.db.models.query.QuerySet.select_related
    https://docs.djangoproject.com/en/1.5/ref/models/querysets/#django.db.models.query.QuerySet.prefetch_related

    :param obj:
    :return:
    """

    comments = None
    if has_comment:
        content_type = ContentType.objects.get_for_model(obj)
        comments = Comment.objects\
            .filter(content_type=content_type, object_pk=obj.pk)

    return {'comments': comments}
