from django.urls import re_path
from fack import views

urlpatterns = [
    re_path(
        r'^$',
        view=views.TopicList.as_view(),
        name='faq_topic_list',
    ),
    re_path(
        r'^search/$',
        view=views.SearchView.as_view(),
        name='faq_search',
    ),
    re_path(
        r'^questions/$',
        view=views.QuestionOverviewList.as_view(),
        name='faq_question_list',
    ),
    re_path(
        r'^detail/(?P<topic_slug>[\w-]+)/(?P<slug>[\w-]+)/helpful$',
        view=views.QuestionHelpfulVote.as_view(),
        name='question_helpful'
    ),
    re_path(
        r'^submit/$',
        view=views.SubmitFAQ.as_view(),
        name='faq_submit',
    ),
    re_path(
        r'^submit/thanks/$',
        view=views.SubmitFAQThanks.as_view(),
        name='faq_submit_thanks',
    ),
    re_path(
        r'^(?P<slug>[\w-]+)/$',
        view=views.TopicDetail.as_view(),
        name='faq_topic_detail',
    ),
    re_path(
        r'^(?P<topic_slug>[\w-]+)/(?P<slug>[\w-]+)/$',
        view=views.QuestionDetail.as_view(),
        name='faq_question_detail',
    ),
]
