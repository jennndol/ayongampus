from django import forms

from ayongampus.questions.models import Answer, Question


class QuestionForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control border-input'}),
        max_length=255)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control border-input'}),
        max_length=2000)
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control border-input tagsinput tag-{blue} tag-fill'}),
        max_length=255,
        required=False,
        help_text='Use tags as much as specific, such as "study, abroad"')

    class Meta:
        model = Question
        fields = ['title', 'description', 'tags']


class AnswerForm(forms.ModelForm):
    question = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                      queryset=Question.objects.all())
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        max_length=2000)

    class Meta:
        model = Answer
        fields = ['question', 'description']
