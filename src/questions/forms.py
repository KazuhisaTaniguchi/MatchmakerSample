from django import forms
from .models import LEVELS, Answer, Question


class UserResponseForm(forms.Form):
    question_id = forms.IntegerField()
    answer_id = forms.IntegerField()
    important_level = forms.ChoiceField(choices=LEVELS)

    their_answer_id = forms.IntegerField()
    their_important_level = forms.ChoiceField(choices=LEVELS)

    def clean_answer_id(self):
        answer_id = self.cleaned_data['answer_id']
        try:
            obj = Answer.objects.get(pk=answer_id)
        except:
            raise forms.ValidationError(
                'There was an error with the answer. Please try agein.')
        return answer_id

    def clean_question_id(self):
        question_id = self.cleaned_data['question_id']
        try:
            obj = Answer.objects.get(pk=question_id)
        except:
            raise forms.ValidationError(
                'There was an error with the question. Please try agein.')
        return question_id

    def clean_their_answer_id(self):
        their_answer_id = self.cleaned_data['their_answer_id']
        try:
            obj = Answer.objects.get(pk=their_answer_id)
        except:
            if their_answer_id == -1:
                return their_answer_id
            else:
                raise forms.ValidationError(
                    'There was an error with the answer provided for them. Please try agein.')
        return their_answer_id
