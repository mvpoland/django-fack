from __future__ import absolute_import

from django.db.models import Max, Sum, Count
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import View, ListView, DetailView, TemplateView, CreateView
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.response import TemplateResponse

from .models import Question, Topic, QuestionScore
from .forms import SubmitFAQForm
from .utils import search

import json


class TopicList(ListView):
    model = Topic
    template_name = "faq/topic_list.html"
    allow_empty = True
    context_object_name = "topics"

    def get_context_data(self, **kwargs):
        data = super(TopicList, self).get_context_data(**kwargs)
        
        # This slightly magical queryset grabs the latest update date for 
        # topic's questions, then the latest date for that whole group.
        # In other words, it's::
        #
        #   max(max(q.updated_on for q in topic.questions) for topic in topics)
        #
        # Except performed in the DB, so quite a bit more efficient.
        #
        # We can't just do Question.objects.all().aggregate(max('updated_on'))
        # because that'd prevent a subclass from changing the view's queryset
        # (or even model -- this view'll even work with a different model
        # as long as that model has a many-to-one to something called "questions"
        # with an "updated_on" field). So this magic is the price we pay for
        # being generic.

        last_updated = data['object_list'].annotate(updated=Max('questions__updated_on'))\
                                          .aggregate(Max('updated'))
        
        data.update({'last_updated': last_updated['updated__max']})

        return data

    def get_queryset(self):
        return Topic.site_objects.filter().order_by('-sort_order')


class TopicDetail(DetailView):
    model = Topic
    template_name = "faq/topic_detail.html"
    context_object_name = "topic"
    
    def get_object(self, queryset=None):
        topic = super(TopicDetail, self).get_object(queryset)
        topic.add_view()
        return topic

    def get_context_data(self, **kwargs):
        # Include a list of questions this user has access to. If the user is
        # logged in, this includes protected questions. Otherwise, not.
        qs = self.object.questions.active()
        if self.request.user.is_anonymous():
            qs = qs.exclude(protected=True)

        data = super(TopicDetail, self).get_context_data(**kwargs)
        data.update({
            'questions': qs,
            'last_updated': qs.aggregate(updated=Max('updated_on'))['updated'],
        })
        return data


class QuestionOverviewList(ListView):
    model = Question
    template_name = "faq/question_list.html"
    allow_empty = True
    context_object_name = "questions"
    queryset = Question.site_objects.all()

    def get_context_data(self, **kwargs):
        return self.get_question_score(**kwargs)

    def get_question_score(self, **kwargs):
        data = super(QuestionOverviewList, self).get_context_data(**kwargs)
        questions = Question.site_objects.active().annotate(
            nb_positive=Sum('questionscore__score'),
            nb_all=Count('questionscore')
        ).order_by('-topic__nr_views')

        for question in questions:
            if question.nb_all > 0:
                percentage = (question.nb_positive or 0)*100.0 / question.nb_all
                question.score = percentage
            else:
                question.score = "NA"

        if kwargs.get('sort') == "score":
            questions = sorted(questions, key=(lambda question: question.score), reverse=True)

        data.update({'questions': questions})
        return data


class QuestionDetail(DetailView):
    is_preview = False
    queryset = Question.site_objects.active()
    template_name = "faq/question_detail.html"

    def _allowed(self, question):
        """
        Allow authenticated admin users to preview a question

        :param question:
        :return:
        """
        if question.is_active() or (self.is_preview and self.request.user.is_staff):
            return True

    def get_object(self, queryset=None):
        question = super(QuestionDetail, self).get_object(queryset)

        if self._allowed(question):
            question.add_view()
            return question

        raise Http404('No question found')

    def get_queryset(self):
        topic = get_object_or_404(Topic, slug=self.kwargs['topic_slug'], site=Site.objects.get_current())

        qs = Question.site_objects.filter(topic=topic)
        if self.request.user.is_anonymous():
            qs = qs.exclude(protected=True)

        return qs


class SubmitFAQ(CreateView):
    model = Question
    form_class = SubmitFAQForm
    template_name = "faq/submit_question.html"
    success_view_name = "faq_submit_thanks"
    
    def get_form_kwargs(self):
        kwargs = super(SubmitFAQ, self).get_form_kwargs()
        kwargs['instance'] = Question()
        if self.request.user.is_authenticated():
            kwargs['instance'].created_by = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super(SubmitFAQ, self).form_valid(form)
        messages.success(self.request, 
            _("Your question was submitted and will be reviewed by for inclusion in the FAQ."),
            fail_silently=True,
        )
        return response
        
    def get_success_url(self):
        # The superclass version raises ImproperlyConfigered if self.success_url
        # isn't set. Instead of that, we'll try to redirect to a named view.
        if self.success_url:
            return self.success_url
        else:
            return reverse(self.success_view_name)


class SubmitFAQThanks(TemplateView):
    template_name = "faq/submit_thanks.html"


class QuestionHelpfulVote(View):
    def post(self, request, topic_slug, slug):
        """
        Scores a question.  The question can only be scored by 0 (not helpful) and 1 (helpful).  A user can score a question
        only once.
         - If the user is logged on we check if he already scored the question
         - If the user is not logged on we check if the ip of the user already scored the question

        :param request:
        :return: a json response
        """
        topic = Topic.site_objects.get(slug=topic_slug)
        question = Question.site_objects.filter(slug=slug, topic=topic)[0]
        data = {}
        user = request.user
        ip_address = request.META.get('REMOTE_ADDR', '')

        if user.is_authenticated():
            qs_user = user
            qs_done = True if len(QuestionScore.objects.filter(question = question, user = user))>0 else False
        else:
            qs_user = None
            qs_done = True if len(QuestionScore.objects.filter(question = question, ip_address = ip_address, user = None))>0 else False

        # optimistic positive score
        if "n" == request.GET.get("q"):
            qs_score = 0
        else:
            qs_score = 1

        if not qs_done:
            question_score = QuestionScore()
            question_score.question = question
            question_score.user = qs_user
            question_score.score = qs_score
            question_score.ip_address = ip_address
            question_score.save()

        return HttpResponse(json.dumps(data), mimetype='application/json')


class SearchView(View):
    template_name = 'faq/search.html'
    redirect_empty_view_name = 'fack.overview'

    def get(self, request):
        query = request.GET.get("q", "").strip()
        data = search(query)

        if not data:
            return HttpResponseRedirect(reverse(self.redirect_empty_view_name))

        return TemplateResponse(request, self.template_name, data)
