from ayongampus.quiz.forms import SubjectAndChapterFormSet
from ayongampus.quiz.models import Quiz
from ayongampus.subject.models import Subject, Chapter
from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import ListView
from django.views.generic import UpdateView


class ChapterAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Chapter.objects.none()

        qs = Chapter.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class SubjectsListView(ListView):
    model = Subject


class ViewQuizListBySubject(ListView):
    model = Quiz
    template_name = 'quiz/view_quiz_subject.html'

    def dispatch(self, request, *args, **kwargs):
        self.subject = get_object_or_404(
            Subject,
            subject=self.kwargs['subject_name']
        )

        return super(ViewQuizListBySubject, self). \
            dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ViewQuizListBySubject, self) \
            .get_context_data(**kwargs)

        context['subject'] = self.subject
        return context

    def get_queryset(self):
        queryset = super(ViewQuizListBySubject, self).get_queryset()
        return queryset.filter(subject=self.subject, draft=False)


def get_user(request):
    return request.user


class SubjectListView(ListView):
    model = Subject
    template_name = "dashboard/subject_list.html"
    context_object_name = "subjects"

    def get_context_data(self, **kwargs):
        context = super(SubjectListView, self).get_context_data(**kwargs)
        context['subjects'] = Subject.objects.filter(author=self.request.user).order_by('-id')
        return context


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


class SubjectChapterCreate(AjaxableResponseMixin, CreateView):
    model = Subject
    fields = ['subject', ]
    success_url = reverse_lazy('core_subject_list')

    def get_context_data(self, **kwargs):
        data = super(SubjectChapterCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['chapters'] = SubjectAndChapterFormSet(self.request.POST)
        else:
            data['chapters'] = SubjectAndChapterFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        chapters = context['chapters']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.author = get_user(self.request)
            self.object.save()
            if chapters.is_valid():
                chapters.instance = self.object
                chapters.save()
        return super(SubjectChapterCreate, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class SubjectChapterUpdate(UpdateView):
    model = Subject
    fields = ['subject']
    success_url = reverse_lazy('core_subject_list')

    def get_context_data(self, **kwargs):
        data = super(SubjectChapterUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['chapters'] = SubjectAndChapterFormSet(self.request.POST, instance=self.object)
        else:
            data['chapters'] = SubjectAndChapterFormSet(instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        chapters = context['chapters']
        with transaction.atomic():
            self.object = form.save()
            if chapters.is_valid():
                chapters.instance = self.object
                chapters.save()
        return super(SubjectChapterUpdate, self).form_valid(form)


class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = "dashboard/delete_form_for_deleteview.html"
    success_url = reverse_lazy('core_subject_list')


def overview(request):
    return render(request, 'dashboard/overview.html')
