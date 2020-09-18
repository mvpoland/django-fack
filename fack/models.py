import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify

from fack.conf import STORAGE
from fack.managers import QuestionManager, SiteQuestionManager, SiteTopicManager


class Topic(models.Model):
    """
    Generic Topics for FAQ question grouping
    """
    site = models.ForeignKey(Site, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(_('name'), max_length=150)
    slug = models.SlugField(_('slug'), max_length=150)
    sort_order = models.IntegerField(_('sort order'), default=0,
        help_text=_('The order you would like the topic to be displayed.'))
    nr_views = models.IntegerField(default=0)
    icon = models.ImageField(upload_to='topic_icons/', storage=STORAGE, null=True, blank=True)
    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'), null=True, blank=True,
                                   related_name="+", on_delete=models.CASCADE)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('updated by'), null=True, blank=True,
                                   related_name="+", on_delete=models.CASCADE)

    objects = models.Manager()
    site_objects = SiteTopicManager()

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        ordering = ['sort_order', 'nr_views', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('faq_topic_detail', args=(self.slug,))

    def add_view(self):
        self.nr_views += 1
        self.save()


class Question(models.Model):
    HEADER = 2
    ACTIVE = 1
    INACTIVE = 0
    STATUS_CHOICES = (
        (ACTIVE, _('Active')),
        (INACTIVE, _('Inactive')),
        (HEADER, _('Group Header')),
    )

    text = models.TextField(_('question'), help_text=_('The actual question itself.'))
    answer = models.TextField(_('answer'), blank=True, help_text=_('The answer text.'))
    topic = models.ForeignKey(Topic, verbose_name=_('topic'), related_name='questions', on_delete=models.CASCADE)
    slug = models.SlugField(_('slug'), max_length=100)
    status = models.IntegerField(_('status'),
        choices=STATUS_CHOICES, default=INACTIVE,
        help_text=_("Only questions with their status set to 'Active' will be "
                    "displayed. Questions marked as 'Group Header' are treated "
                    "as such by views and templates that are set up to use them."))

    protected = models.BooleanField(_('is protected'), default=False,
        help_text=_("Set true if this question is only visible by authenticated users."))

    sort_order = models.IntegerField(_('sort order'), default=0,
        help_text=_('The order you would like the question to be displayed.'))

    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    updated_on = models.DateTimeField(_('updated on'), auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('created by'),
        null=True, blank=True, related_name="+", on_delete=models.CASCADE)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('updated by'),
        null=True, blank=True, related_name="+", on_delete=models.CASCADE)
    nr_views = models.IntegerField(default=0)

    objects = QuestionManager()
    site_objects = SiteQuestionManager()

    class Meta:
        verbose_name = _("Frequent asked question")
        verbose_name_plural = _("Frequently asked questions")
        ordering = ['sort_order', 'nr_views', 'created_on']

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('faq_question_detail', args=(self.topic.slug, self.slug))

    def save(self, *args, **kwargs):
        # Set the date updated.
        self.updated_on = datetime.datetime.now()

        # Create a unique slug, if needed.
        if not self.slug:
            suffix = 0
            potential = base = slugify(self.text[:90])
            while not self.slug:
                if suffix:
                    potential = "{}-{}".format(base, suffix)
                if not Question.objects.filter(slug=potential).exists():
                    self.slug = potential
                # We hit a conflicting slug; increment the suffix and try again.
                suffix += 1

        super(Question, self).save(*args, **kwargs)

    def is_header(self):
        return self.status == Question.HEADER

    def is_active(self):
        return self.status == Question.ACTIVE

    def add_view(self):
        self.nr_views += 1
        self.save()
        self.topic.add_view()


SCORE_CHOICES = (
    (0, "No"),
    (1, "Yes")
)


class QuestionScore(models.Model):
    """

    """
    score = models.IntegerField(_("score"), choices=SCORE_CHOICES, default=1)
    question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, verbose_name='IP address',
                                              blank=True, null=True)

    def __str__(self):
        return self.question.text
