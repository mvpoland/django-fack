from datatrans.utils import register

from fack.models import Topic, Question

##
## Works for django-datatrans==0.1.5
## https://github.com/vikingco/django-datatrans
##


class TopicTranslation(object):
    fields = ('name',)
register(Topic, TopicTranslation)


class QuestionTranslation(object):
    fields = ('text', 'answer')
register(Question, QuestionTranslation)
