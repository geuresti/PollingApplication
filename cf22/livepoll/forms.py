from django import forms
from .models import Poll, Answer

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('title', 'question',)

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)
