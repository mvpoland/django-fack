"""
Some basic admin tests.

Rather than testing the frontend UI -- that's be a job for something like
Selenium -- this does a bunch of mocking and just tests the various admin
callbacks.
"""

from __future__ import absolute_import

import mock
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.http import HttpRequest
from django import forms
from ..admin import QuestionAdmin
from ..models import Question


class FAQAdminTests(TestCase):

    def test_question_admin_save_model(self):
        user = get_user_model()
        user1 = mock.Mock(spec=user)
        user2 = mock.Mock(spec=user)
        req = mock.Mock(spec=HttpRequest)
        obj = mock.Mock(spec=Question)
        form = mock.Mock(spec=forms.Form)

        qa = QuestionAdmin(Question, admin.site)

        # Test saving a new model.
        req.user = user1
        qa.save_model(req, obj, form, change=False)
        self.assertEqual(obj.save.call_count, 1)
        self.assertEqual(obj.created_by, user1, "created_by wasn't set to request.user")
        self.assertEqual(obj.updated_by, user1, "updated_by wasn't set to request.user")

        # And saving an existing model.
        obj.save.reset_mock()
        req.user = user2
        qa.save_model(req, obj, form, change=True)
        self.assertEqual(obj.save.call_count, 1)
        self.assertEqual(obj.created_by, user1, "created_by shouldn't have been changed")
        self.assertEqual(obj.updated_by, user2, "updated_by wasn't set to request.user")
