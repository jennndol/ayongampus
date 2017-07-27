from ayongampus.quiz.models import Quiz
from ayongampus.quiz.multichoice.models import MCQuestion
from ayongampus.subject.models import Subject, Chapter
from django import forms
from django.forms import ModelForm, inlineformset_factory, Form
from django.forms.widgets import RadioSelect, Textarea


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        exclude = []


class ChapterForm(ModelForm):
    class Meta:
        model = Chapter
        exclude = []


SubjectAndChapterFormSet = inlineformset_factory(Subject, Chapter,
                                                 form=ChapterForm, extra=1)


class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        exclude = ('author',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(QuizForm, self).__init__(*args, **kwargs)
        self.fields['subject'].queryset = Subject.objects.filter(author=user)


class ChoiceForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        # print question._meta
        # print question.get_answers_list()
        # print question.correct_answers_number()
        if question.correct_answers_number() == 1:
            super(ChoiceForm, self).__init__(*args, **kwargs)
            choice_list = [x for x in question.get_answers_list()]
            self.fields["answers"] = forms.ChoiceField(choices=choice_list,
                                                       widget=RadioSelect)

        else:
            super(ChoiceForm, self).__init__(*args, **kwargs)
            choice_list = [x for x in question.get_answers_list()]
            self.fields["answers"] = forms.MultipleChoiceField(choices=choice_list,
                                                               widget=forms.CheckboxSelectMultiple())


class EssayForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(EssayForm, self).__init__(*args, **kwargs)
        self.fields["answers"] = forms.CharField(
            widget=Textarea(attrs={
                'style': 'width:100%',
                'placeholder': 'text everything to reply the question of "' + str(question) + '"',
            }))


class AddQuestionsForm(Form):
    questions = forms.ModelMultipleChoiceField(required=False, queryset={}, label="Questions to choose", )

    def __init__(self, *args, **kwargs):
        self.questions = kwargs.pop('questions', None)
        super(AddQuestionsForm, self).__init__(*args, **kwargs)
        self.fields['questions'].queryset = self.questions


class MCQuestionForm(forms.ModelForm):
    class Meta:
        model = MCQuestion
        fields = ('chapter', 'content', 'explanation')
