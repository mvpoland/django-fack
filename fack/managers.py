from django.db import models
from django.db.models.query import QuerySet
from django.contrib.sites.models import Site


class SiteTopicManager(models.Manager):
    def get_query_set(self):
        queryset = super(SiteTopicManager, self).get_query_set()
        site = Site.objects.get_current()
        return queryset.filter(site=site)


class SiteQuestionManager(models.Manager):
    def get_query_set(self):
        site = Site.objects.get_current()
        return QuestionQuerySet(self.model).filter(topic__site=site)

    def active(self):
        return self.get_query_set().active()


class QuestionQuerySet(QuerySet):
    def active(self):
        """
        Return only "active" (i.e. published) questions.
        """
        return self.filter(status__exact=self.model.ACTIVE)


class QuestionManager(models.Manager):
    def get_query_set(self):
        return QuestionQuerySet(self.model)

    def active(self):
        return self.get_query_set().active()
