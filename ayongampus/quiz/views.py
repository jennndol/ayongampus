import random

import xlwt
from ayongampus.quiz.essay.models import Essay_Question
from ayongampus.quiz.forms import AddQuestionsForm
from ayongampus.quiz.forms import QuizForm
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils import formats
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView
from django.views.generic import DetailView, ListView, TemplateView, FormView

from .forms import ChoiceForm, EssayForm
from .models import Quiz, Progress, Sitting, Question


class QuestionListView(ListView):
    model = Question
    template_name = "dashboard/question_list.html"

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        context['questions'] = Question.objects.filter(chapter__subject__author=self.request.user).order_by(
            '-created_at')
        return context


class QuizQuestionCreateView(FormView):
    template_name = "dashboard/add_questions_to_quiz.html"
    form_class = AddQuestionsForm

    def get_form_kwargs(self):
        quiz = Quiz.objects.get(pk=self.kwargs['pk'])
        subject = quiz.subject
        kwargs = super(QuizQuestionCreateView, self).get_form_kwargs()
        q_id_list = set([question.id for question in quiz.question_set.all()])
        kwargs['questions'] = Question.objects.filter(chapter__subject=subject).exclude(pk__in=q_id_list).order_by(
            'created_at')
        return kwargs

    def form_valid(self, form):
        questions = form.cleaned_data['questions']
        quiz = Quiz.objects.get(pk=self.kwargs['pk'])
        question_list = Question.objects.filter(pk__in=questions)
        for question in question_list:
            quiz.question_set.add(question)

        return redirect('core_question_add', pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        """
        Use this to add extra context.
        """
        context = super(QuizQuestionCreateView, self).get_context_data(**kwargs)
        quiz = Quiz.objects.get(pk=self.kwargs['pk'])
        chosen_questions = quiz.question_set.all()
        print chosen_questions
        context['quiz'] = quiz
        context['questions'] = quiz.question_set.all().order_by('-created_at')
        return context


def remove_question_from_quiz(request, pk_quiz, pk_question):
    quiz = Quiz.objects.get(pk=pk_quiz)
    question = Question.objects.get(pk=pk_question)
    quiz.question_set.remove(question)
    return redirect("/dashboard/quizzes/" + str(quiz.pk) + "/q")


class QuestionDeleteView(DeleteView):
    model = Question
    template_name = "dashboard/delete_form_for_deleteview.html"
    success_url = '/dashboard/questions'


def quiz_list(request):
    quizzes = Quiz.objects.filter(author=request.user)
    return render(request, 'dashboard/quiz_list.html', {'quizzes': quizzes})


def save_quiz_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.author = request.user
            quiz.save()
            data['form_is_valid'] = True
            quizzes = Quiz.objects.filter(author=request.user)
            data['html_quiz_list'] = render_to_string('dashboard/includes/partial_quiz_list.html', {
                'quizzes': quizzes
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def quiz_create(request):
    if request.method == 'POST':
        form = QuizForm(request.POST, user=request.user)
    else:
        form = QuizForm(user=request.user)
    return save_quiz_form(request, form, 'dashboard/includes/partial_quiz_create.html')


def quiz_update(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz, user=request.user)
    else:
        form = QuizForm(instance=quiz, user=request.user)
    return save_quiz_form(request, form, 'dashboard/includes/partial_quiz_update.html')


def quiz_delete(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    data = dict()
    if request.method == 'POST':
        quiz.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        quizzes = Quiz.objects.all()
        data['html_quiz_list'] = render_to_string('dashboard/includes/partial_quiz_list.html', {
            'quizzes': quizzes
        })
    else:
        context = {'quiz': quiz}
        data['html_form'] = render_to_string('dashboard/includes/partial_quiz_delete.html',
                                             context,
                                             request=request,
                                             )
    return JsonResponse(data)


def quiz_detail(request, slug):
    quiz = Quiz.objects.get(url=slug)
    return render(request, 'dashboard/quiz_detail.html', {'quiz': quiz})


def export_scores_xls(request, pk):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Scores')
    q = Quiz.objects.get(pk=pk)

    ws.write(0, 0, 'Quiz : ' + q.title)
    ws.write(0, 3, 'Subject : ' + q.subject.subject)

    # Sheet header, first row
    row_num = 3

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['User', 'Score', 'Success', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Sitting.objects.filter(quiz=q)
    for row in rows:
        row_num += 1
        is_success = False
        if row.get_percent_correct >= row.quiz.pass_mark:
            is_success = True

        row = [
            row.user.profile.get_screen_name(),
            row.get_percent_correct,
            is_success,
            formats.date_format(row.end, "DATE_FORMAT"),
        ]
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


class QuizMarkerMixin(object):
    @method_decorator(login_required)
    @method_decorator(permission_required('quiz.view_sittings'))
    def dispatch(self, *args, **kwargs):
        return super(QuizMarkerMixin, self).dispatch(*args, **kwargs)


class SittingFilterTitleMixin(object):
    def get_queryset(self):
        queryset = super(SittingFilterTitleMixin, self).get_queryset()
        quiz_filter = self.request.GET.get('quiz_filter')
        if quiz_filter:
            queryset = queryset.filter(quiz__title__icontains=quiz_filter)

        return queryset


class QuizListView(ListView):
    model = Quiz

    def get_queryset(self):
        queryset = super(QuizListView, self).get_queryset()
        return queryset.filter(draft=False)


class QuizDetailView(DetailView):
    model = Quiz
    slug_field = 'url'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class QuizUserProgressView(TemplateView):
    template_name = 'quiz/progress.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(QuizUserProgressView, self) \
            .dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuizUserProgressView, self).get_context_data(**kwargs)
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        context['cat_scores'] = progress.list_all_cat_scores
        context['exams'] = progress.show_exams()
        return context


class QuizMarkingList(QuizMarkerMixin, SittingFilterTitleMixin, ListView):
    model = Sitting

    def get_queryset(self):
        queryset = super(QuizMarkingList, self).get_queryset().filter(complete=True, quiz__author=self.request.user)

        user_filter = self.request.GET.get('user_filter')
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter, quiz__author=self.request.user)

        return queryset


class QuizMarkingDetail(QuizMarkerMixin, DetailView):
    model = Sitting

    def post(self, request, *args, **kwargs):
        sitting = self.get_object()

        q_to_toggle = request.POST.get('qid', None)
        if q_to_toggle:
            q = Question.objects.get_subclass(id=int(q_to_toggle))
            if int(q_to_toggle) in sitting.get_incorrect_questions:
                sitting.remove_incorrect_question(q)
            else:
                sitting.add_incorrect_question(q)

        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super(QuizMarkingDetail, self).get_context_data(**kwargs)
        context['questions'] = \
            context['sitting'].get_questions(with_answers=True)
        return context

        # Check later


class QuizTake(FormView):
    form_class = ChoiceForm
    template_name = 'quiz/question.html'

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, url=self.kwargs['quiz_name'])
        if self.quiz.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        self.logged_in_user = self.request.user.is_authenticated()

        if self.logged_in_user:
            self.sitting = Sitting.objects.user_sitting(request.user,
                                                        self.quiz)
        else:
            self.sitting = self.anon_load_sitting()

        if self.sitting is False:
            return render(request, 'quiz/single_complete.html')

        return super(QuizTake, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class=ChoiceForm):
        if self.logged_in_user:
            self.question = self.sitting.get_first_question()
            self.progress = self.sitting.progress()
        else:
            self.question = self.anon_next_question()
            self.progress = self.anon_sitting_progress()

        if self.question.__class__ is Essay_Question:
            form_class = EssayForm

        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizTake, self).get_form_kwargs()

        return dict(kwargs, question=self.question)

    def form_valid(self, form):
        if self.logged_in_user:
            self.form_valid_user(form)
            if self.sitting.get_first_question() is False:
                return self.final_result_user()
        else:
            self.form_valid_anon(form)
            if not self.request.session[self.quiz.anon_q_list()]:
                return self.final_result_anon()

        self.request.POST = {}

        return super(QuizTake, self).get(self, self.request)

    def get_context_data(self, **kwargs):
        context = super(QuizTake, self).get_context_data(**kwargs)
        context['question'] = self.question
        context['quiz'] = self.quiz
        if hasattr(self, 'previous'):
            context['previous'] = self.previous
        if hasattr(self, 'progress'):
            context['progress'] = self.progress
        return context

    def form_valid_user(self, form):
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        guess = form.cleaned_data['answers']
        is_correct = self.question.check_if_correct(guess)

        if is_correct is True:
            self.sitting.add_to_score(1)
            progress.update_score(self.question, 1, 1)
        else:
            self.sitting.add_incorrect_question(self.question)
            progress.update_score(self.question, 0, 1)

        if self.quiz.answers_at_end is not True:
            self.previous = {'previous_answer': guess,
                             'previous_outcome': is_correct,
                             'previous_question': self.question,
                             'answers': self.question.get_answers(),
                             'question_type': {self.question
                                                   .__class__.__name__: True}}
        else:
            self.previous = {}

        self.sitting.add_user_answer(self.question, guess)
        self.sitting.remove_first_question()

    def final_result_user(self):
        results = {
            'quiz': self.quiz,
            'score': self.sitting.get_current_score,
            'max_score': self.sitting.get_max_score,
            'percent': self.sitting.get_percent_correct,
            'sitting': self.sitting,
            'previous': self.previous,
        }

        self.sitting.mark_quiz_complete()

        if self.quiz.answers_at_end:
            results['questions'] = \
                self.sitting.get_questions(with_answers=True)
            results['incorrect_questions'] = \
                self.sitting.get_incorrect_questions

        if self.quiz.exam_paper is False:
            self.sitting.delete()

        return render(self.request, 'quiz/result.html', results)

    def anon_load_sitting(self):
        if self.quiz.single_attempt is True:
            return False

        if self.quiz.anon_q_list() in self.request.session:
            return self.request.session[self.quiz.anon_q_list()]
        else:
            return self.new_anon_quiz_session()

    def new_anon_quiz_session(self):
        """
        Sets the session variables when starting a quiz for the first time
        as a non signed-in user
        """
        self.request.session.set_expiry(259200)  # expires after 3 days
        questions = self.quiz.get_questions()
        question_list = [question.id for question in questions]

        if self.quiz.random_order is True:
            random.shuffle(question_list)

        if self.quiz.max_questions and (self.quiz.max_questions
                                            < len(question_list)):
            question_list = question_list[:self.quiz.max_questions]

        # session score for anon users
        self.request.session[self.quiz.anon_score_id()] = 0

        # session list of questions
        self.request.session[self.quiz.anon_q_list()] = question_list

        # session list of question order and incorrect questions
        self.request.session[self.quiz.anon_q_data()] = dict(
            incorrect_questions=[],
            order=question_list,
        )

        return self.request.session[self.quiz.anon_q_list()]

    def anon_next_question(self):
        next_question_id = self.request.session[self.quiz.anon_q_list()][0]
        return Question.objects.get_subclass(id=next_question_id)

    def anon_sitting_progress(self):
        total = len(self.request.session[self.quiz.anon_q_data()]['order'])
        answered = total - len(self.request.session[self.quiz.anon_q_list()])
        return (answered, total)

    def form_valid_anon(self, form):
        guess = form.cleaned_data['answers']
        is_correct = self.question.check_if_correct(guess)

        if is_correct:
            self.request.session[self.quiz.anon_score_id()] += 1
            anon_session_score(self.request.session, 1, 1)
        else:
            anon_session_score(self.request.session, 0, 1)
            self.request \
                .session[self.quiz.anon_q_data()]['incorrect_questions'] \
                .append(self.question.id)

        self.previous = {}
        if self.quiz.answers_at_end is not True:
            self.previous = {'previous_answer': guess,
                             'previous_outcome': is_correct,
                             'previous_question': self.question,
                             'answers': self.question.get_answers(),
                             'question_type': {self.question
                                                   .__class__.__name__: True}}

        self.request.session[self.quiz.anon_q_list()] = \
            self.request.session[self.quiz.anon_q_list()][1:]

    def final_result_anon(self):
        score = self.request.session[self.quiz.anon_score_id()]
        q_order = self.request.session[self.quiz.anon_q_data()]['order']
        max_score = len(q_order)
        percent = int(round((float(score) / max_score) * 100))
        session, session_possible = anon_session_score(self.request.session)
        if score is 0:
            score = "0"

        results = {
            'score': score,
            'max_score': max_score,
            'percent': percent,
            'session': session,
            'possible': session_possible
        }

        del self.request.session[self.quiz.anon_q_list()]

        if self.quiz.answers_at_end:
            results['questions'] = sorted(
                self.quiz.question_set.filter(id__in=q_order)
                    .select_subclasses(),
                key=lambda q: q_order.index(q.id))

            results['incorrect_questions'] = (
                self.request
                    .session[self.quiz.anon_q_data()]['incorrect_questions'])

        else:
            results['previous'] = self.previous

        del self.request.session[self.quiz.anon_q_data()]

        return render(self.request, 'quiz/result.html', results)


def anon_session_score(session, to_add=0, possible=0):
    """
    Returns the session score for non-signed in users.
    If number passed in then add this to the running total and
    return session score.

    examples:
        anon_session_score(1, 1) will add 1 out of a possible 1
        anon_session_score(0, 2) will add 0 out of a possible 2
        x, y = anon_session_score() will return the session score
                                    without modification

    Left this as an individual function for unit testing
    """
    if "session_score" not in session:
        session["session_score"], session["session_score_possible"] = 0, 0

    if possible > 0:
        session["session_score"] += to_add
        session["session_score_possible"] += possible

    return session["session_score"], session["session_score_possible"]
