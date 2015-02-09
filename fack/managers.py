from django.db import models
from django.db.models.query import QuerySet
from django.contrib.sites.models import Site


class SiteTopicManager(models.Manager):
    def get_queryset(self):
        queryset = super(SiteTopicManager, self).get_queryset()
        site = Site.objects.get_current()
        return queryset.filter(site=site)


class SiteQuestionManager(models.Manager):
    def get_queryset(self):
        site = Site.objects.get_current()
        return QuestionQuerySet(self.model).filter(topic__site=site)

    def active(self):
        return self.get_queryset().active()


class QuestionQuerySet(QuerySet):
    def active(self):
        """
        Return only "active" (i.e. published) questions.
        """
        return self.filter(status__exact=self.model.ACTIVE)


class QuestionManager(models.Manager):
    def get_queryset(self):
        return QuestionQuerySet(self.model)

    def active(self):
        return self.get_queryset().active()
