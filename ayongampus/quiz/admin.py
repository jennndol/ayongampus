from ayongampus.quiz.essay.models import Essay_Question
from ayongampus.quiz.multichoice.models import Answer, MCQuestion
from ayongampus.quiz.truefalse.models import TF_Question
from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Quiz, Subject, Chapter, Progress, Question


class AnswerInline(admin.TabularInline):
    model = Answer


class QuizAdminForm(forms.ModelForm):
    """
    below is from
    http://stackoverflow.com/questions/11657682/
    django-admin-interface-using-horizontal-filter-with-
    inline-manytomany-field
    """

    class Meta:
        model = Quiz
        exclude = []

    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all().select_subclasses(),
        required=False,
        label=_("Questions"),
        widget=FilteredSelectMultiple(
            verbose_name=_("Questions"),
            is_stacked=False))

    def __init__(self, *args, **kwargs):
        super(QuizAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].initial = \
                self.instance.question_set.all().select_subclasses()

    def save(self, commit=True):
        quiz = super(QuizAdminForm, self).save(commit=False)
        quiz.save()
        quiz.question_set = self.cleaned_data['questions']
        self.save_m2m()
        return quiz


class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm

    list_display = ('title', 'subject',)
    list_filter = ('subject',)
    search_fields = ('description', 'subject',)


class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject


class SubjectAdmin(ImportExportModelAdmin):
    search_fields = ('subject',)
    resource_class = SubjectResource


class ChapterResource(resources.ModelResource):
    class Meta:
        model = Chapter


class ChapterAdmin(ImportExportModelAdmin):
    search_fields = ('chapter',)
    list_display = ('chapter', 'subject',)
    list_filter = ('subject',)
    resource_class = ChapterResource


class MCQuestionResource(resources.ModelResource):
    class Meta:
        model = MCQuestion


class MCQuestionAdmin(ImportExportModelAdmin):
    list_display = ('content', 'chapter',)
    list_filter = ('chapter',)
    fields = ('content', 'chapter', 'figure', 'quiz', 'explanation', 'answer_order')

    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)

    inlines = [AnswerInline]

    resource_class = MCQuestionResource


class ProgressAdmin(admin.ModelAdmin):
    """
    to do:
            create a user section
    """
    search_fields = ('user', 'score',)


class TFQuestionResource(resources.ModelResource):
    class Meta:
        model = TF_Question


class TFQuestionAdmin(ImportExportModelAdmin):
    list_display = ('content', 'chapter',)
    list_filter = ('chapter',)
    fields = ('content', 'chapter',
              'figure', 'quiz', 'explanation', 'correct')

    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)
    resource_class = TFQuestionResource


class EssayQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'chapter',)
    list_filter = ('chapter',)
    fields = ('content', 'chapter', 'quiz', 'explanation')
    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(MCQuestion, MCQuestionAdmin)
admin.site.register(Progress, ProgressAdmin)
admin.site.register(TF_Question, TFQuestionAdmin)
admin.site.register(Essay_Question, EssayQuestionAdmin)
