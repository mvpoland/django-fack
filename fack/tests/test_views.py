from __future__ import absolute_import

import django.test
import mock
import os
from django.conf import settings
from fack.models import Topic, Question


class FAQViewTests(django.test.TestCase):
    fixtures = ['faq_test_data.json']

    def setUp(self):
        # Make some test templates available.
        self._oldtd = settings.TEMPLATES[0]['DIRS']
        settings.TEMPLATES[0]['DIRS'] = (
                settings.TEMPLATES[0]['DIRS'] +
                [os.path.join(os.path.dirname(__file__), 'templates')] +
                [os.path.join(os.path.dirname(__file__), '..', 'templates')]
        )

    def tearDown(self):
        settings.TEMPLATES[0]['DIRS'] = self._oldtd

    def test_submit_faq_get(self):
        response = self.client.get('/faq/submit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "faq/submit_question.html")

    @mock.patch('fack.views.messages')
    def test_submit_faq_post(self, mock_messages):
        data = {
            'topic': '1',
            'text': 'What is your favorite color?',
            'answer': 'Blue. I mean red. I mean *AAAAHHHHH....*',
        }
        response = self.client.post('/faq/submit/', data)
        self.assertEqual(mock_messages.success.call_count, 1)
        self.assertRedirects(response, "/faq/submit/thanks/")
        self.assert_(
            Question.objects.filter(text=data['text']).exists(),
            "Expected question object wasn't created."
        )

    def test_submit_thanks(self):
        response = self.client.get('/faq/submit/thanks/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "faq/submit_thanks.html")

    def test_faq_index(self):
        response = self.client.get('/faq/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "faq/topic_list.html")
        topics = response.context["topics"]
        self.assertEqual(2, len(topics))
        self.assertEqual(topics[0].name, 'Serious questions')
        self.assertEqual(topics[1].name, 'Silly questions')
        self.assertEqual(
            response.context['last_updated'],
            Question.objects.order_by('-updated_on')[0].updated_on
        )

    def test_topic_detail(self):
        response = self.client.get('/faq/silly-questions/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "faq/topic_detail.html")
        self.assertEqual(
            response.context['topic'],
            Topic.objects.get(slug="silly-questions")
        )
        self.assertEqual(
            response.context['last_updated'],
            Topic.objects.get(slug='silly-questions').questions.order_by('-updated_on')[0].updated_on
        )
        self.assertQuerysetEqual(
            response.context["questions"],
            ["<Question: What is your favorite color?>",
             "<Question: What is your quest?>"]
        )

    def test_question_detail(self):
        response = self.client.get('/faq/silly-questions/your-quest/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "faq/question_detail.html")
        self.assertEqual(
            response.context["question"],
            Question.objects.get(slug="your-quest")
        )
