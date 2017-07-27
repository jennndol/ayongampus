from ayongampus.quiz.essay.models import Essay_Question
from ayongampus.subject.models import Chapter
from ayongampus.subject.views import get_user
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.views.generic import CreateView
from django.views.generic import UpdateView


class EssayQuestionCreateView(CreateView):
    model = Essay_Question
    fields = ['chapter', 'content', 'explanation']
    success_url = reverse_lazy('core_question_list')

    def get_chapter_list(self):
        return Chapter.objects.filter(subject__author=self.request.user)

    def get_form(self, form_class=None):
        form = super(EssayQuestionCreateView, self).get_form(form_class)
        form.fields['chapter'].queryset = self.get_chapter_list()
        return form

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.author = get_user(self.request)
            self.object.save()
        return super(EssayQuestionCreateView, self).form_valid(form)


class EssayQuestionUpdateView(UpdateView):
    model = Essay_Question
    fields = ['chapter', 'content', 'explanation']
    success_url = reverse_lazy('core_question_list')

    def get_chapter_list(self):
        return Chapter.objects.filter(subject__author=self.request.user)

    def get_form(self, form_class=None):
        form = super(EssayQuestionUpdateView, self).get_form(form_class)
        form.fields['chapter'].queryset = self.get_chapter_list()
        return form

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.author = get_user(self.request)
            self.object.save()
        return super(EssayQuestionUpdateView, self).form_valid(form)
