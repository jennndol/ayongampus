from ayongampus.quiz.multichoice.models import MCQuestion, Answer
from ayongampus.subject.models import Chapter
from django.forms import ModelForm, inlineformset_factory


class MCQuestionForm(ModelForm):
    class Meta:
        model = MCQuestion
        fields = ()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MCQuestionForm, self).__init__(*args, **kwargs)
        self.fields['chapter'].queryset = Chapter.objects.filter(author=user)


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        exclude = ()


MCQuestionAnswerFormSet = inlineformset_factory(MCQuestion, Answer,
                                                form=AnswerForm, extra=1)
