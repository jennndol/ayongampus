from ayongampus.quiz.essay.models import Essay_Question
from django.forms import ModelForm


class EssayForm(ModelForm):
    class Meta:
        model = Essay_Question
        exclude = ()
