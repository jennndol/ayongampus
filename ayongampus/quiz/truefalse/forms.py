from ayongampus.quiz.truefalse.models import TF_Question
from dal import autocomplete
from django.forms import ModelForm


class TFQuestionForm(ModelForm):
    class Meta:
        model = TF_Question
        exclude = ('quiz', 'figure')
        widgets = {
            'chapter': autocomplete.ModelSelect2(url='chapter-autocomplete')
        }
