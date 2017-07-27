from ayongampus.quiz.multichoice.forms import MCQuestionAnswerFormSet
from ayongampus.quiz.multichoice.models import MCQuestion
from ayongampus.subject.models import Chapter
from ayongampus.subject.views import get_user
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic import UpdateView


class MCQuestionAnswerCreate(CreateView):
    model = MCQuestion
    fields = ['chapter', 'content', 'explanation']

    success_url = reverse_lazy('core_question_list')

    def get_chapter_list(self):
        return Chapter.objects.filter(subject__author=self.request.user)

    def get_form(self, form_class=None):
        form = super(MCQuestionAnswerCreate, self).get_form(form_class)
        form.fields['chapter'].queryset = self.get_chapter_list()
        return form

    def get_context_data(self, **kwargs):
        data = super(MCQuestionAnswerCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['answers'] = MCQuestionAnswerFormSet(self.request.POST)
        else:
            data['answers'] = MCQuestionAnswerFormSet()

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        answers = context['answers']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.author = get_user(self.request)
            self.object.save()
            if answers.is_valid():
                answers.instance = self.object
                answers.save()
        return super(MCQuestionAnswerCreate, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class MCQuestionAnswerUpdate(UpdateView):
    model = MCQuestion
    fields = ['chapter', 'content', 'explanation']

    success_url = reverse_lazy('core_question_list')

    def get_chapter_list(self):
        return Chapter.objects.filter(subject__author=self.request.user)

    def get_form(self, form_class=None):
        form = super(MCQuestionAnswerUpdate, self).get_form(form_class)
        form.fields['chapter'].queryset = self.get_chapter_list()
        return form

    def get_context_data(self, **kwargs):
        data = super(MCQuestionAnswerUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['answers'] = MCQuestionAnswerFormSet(self.request.POST, instance=self.object)
        else:
            data['answers'] = MCQuestionAnswerFormSet(instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        answers = context['answers']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.author = get_user(self.request)
            self.object.save()
            if answers.is_valid():
                answers.instance = self.object
                answers.save()
        return super(MCQuestionAnswerUpdate, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)
