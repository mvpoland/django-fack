from django.conf.urls import url
from fack import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.TopicList.as_view(),
        name='faq_topic_list',
    ),
    url(
        regex=r'^search/$',
        view=views.SearchView.as_view(),
        name='faq_search',
    ),
    url(
        regex=r'^questions/$',
        view=views.QuestionOverviewList.as_view(),
        name='faq_question_list',
    ),
    url(
        regex=r'^detail/(?P<topic_slug>[\w-]+)/(?P<slug>[\w-]+)/helpful$',
        view=views.QuestionHelpfulVote.as_view(),
        name='question_helpful'
    ),
    url(
        regex=r'^submit/$',
        view=views.SubmitFAQ.as_view(),
        name='faq_submit',
    ),
    url(
        regex=r'^submit/thanks/$',
        view=views.SubmitFAQThanks.as_view(),
        name='faq_submit_thanks',
    ),
    url(
        regex=r'^(?P<slug>[\w-]+)/$',
        view=views.TopicDetail.as_view(),
        name='faq_topic_detail',
    ),
    url(
        regex=r'^(?P<topic_slug>[\w-]+)/(?P<slug>[\w-]+)/$',
        view=views.QuestionDetail.as_view(),
        name='faq_question_detail',
    ),
]
