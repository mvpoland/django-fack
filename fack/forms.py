"""
Here we define a form for allowing site users to submit a potential FAQ that
they would like to see added.

From the user's perspective the question is not added automatically, but
actually it is, only it is added as inactive.
"""
from django import forms
from fack.models import Question


class SubmitFAQForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['topic', 'text', 'answer']
