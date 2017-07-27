from ayongampus.quiz.truefalse.models import TF_Question
from ayongampus.subject.models import Chapter
from ayongampus.subject.views import get_user
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.views.generic import CreateView
from django.views.generic import UpdateView


class TFQuestionCreateView(CreateView):
    model = TF_Question
    fields = ['chapter', 'content', 'correct', 'explanation']
    success_url = reverse_lazy('core_question_list')

    def get_chapter_list(self):
        return Chapter.objects.filter(subject__author=self.request.user)

    def get_form(self, form_class=None):
        form = super(TFQuestionCreateView, self).get_form(form_class)
        form.fields['chapter'].queryset = self.get_chapter_list()
        return form

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.author = get_user(self.request)
            self.object.save()
        return super(TFQuestionCreateView, self).form_valid(form)


class TFQuestionUpdateView(UpdateView):
    model = TF_Question
    fields = ['chapter', 'content', 'correct', 'explanation']
    success_url = reverse_lazy('core_question_list')

    def get_chapter_list(self):
        return Chapter.objects.filter(subject__author=self.request.user)

    def get_form(self, form_class=None):
        form = super(TFQuestionUpdateView, self).get_form(form_class)
        form.fields['chapter'].queryset = self.get_chapter_list()
        return form

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.author = get_user(self.request)
            self.object.save()
        return super(TFQuestionUpdateView, self).form_valid(form)
