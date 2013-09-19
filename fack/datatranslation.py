from datatrans.utils import register

from fack.models import Topic, Question


class TopicTranslation(object):
    fields = ('name',)
register(Topic, TopicTranslation)


class QuestionTranslation(object):
    fields = ('text', 'answer')
register(Question, QuestionTranslation)
