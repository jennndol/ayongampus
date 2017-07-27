from django import forms

from ayongampus.articles.models import Article


class ArticleForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control border-input'}),
        max_length=255)
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control border-input'}))
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control tagsinput tag-{blue} tag-fill border-input'}),
        max_length=255, required=False,
        help_text='Use tag as much as specific "study, abroad"'
    )  # noqa: E501

    class Meta:
        model = Article
        fields = ['title', 'content', 'tags', 'status']
