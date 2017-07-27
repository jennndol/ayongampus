from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from ayongampus.quiz.models import Question


def answer_list_validation(x, y):
    return sorted(x) == sorted(y)


def is_list(x):
    return not isinstance(x, basestring)


ANSWER_ORDER_OPTIONS = (
    ('content', _('Content')),
    ('random', _('Random')),
    ('none', _('None'))
)


class MCQuestion(Question):
    answer_order = models.CharField(
        max_length=30, null=True, blank=True,
        choices=ANSWER_ORDER_OPTIONS,
        help_text=_("The order in which multichoice "
                    "answer options are displayed "
                    "to the user"),
        verbose_name=_("Answer Order"))

    def check_if_correct(self, guess):
        if is_list(guess):
            correct_answer_list = self.get_correct_answers_unicode_list()
            guess = [guess.encode("utf8") for guess in
                     guess]
            if answer_list_validation(correct_answer_list, guess) == True:
                return True
            else:
                return False

        else:
            answer = Answer.objects.get(id=guess)
            if answer.correct is True:
                return True
            else:
                return False

    def order_answers(self, queryset):
        if self.answer_order == 'content':
            return queryset.order_by('content')
        if self.answer_order == 'random':
            return queryset.order_by('?')
        if self.answer_order == 'none':
            return queryset.order_by()
        return queryset

    def get_answers(self):
        return self.order_answers(Answer.objects.filter(question=self))

    def get_correct_answers(self):
        return self.get_answers().filter(correct=True)

    def correct_answers_number(self):
        return self.get_correct_answers().count()

    def get_answers_list(self):
        return [(answer.id, answer.content) for answer in
                self.get_answers()]

    def get_correct_answers_unicode_list(self):
        return [(str(answer)) for answer in
                self.get_correct_answers().values_list('id', flat=True)]

    def answer_choice_to_string(self, guess):
        if is_list(guess):
            answers = Answer.objects.filter(id__in=guess)
            return [(str(answer)) for answer in answers.values_list('content', flat=True)]
        else:
            return Answer.objects.get(id=guess).content

    class Meta:
        verbose_name = _("Multiple Choice Question")
        verbose_name_plural = _("Multiple Choice Questions")


@python_2_unicode_compatible
class Answer(models.Model):
    question = models.ForeignKey(MCQuestion, verbose_name=_("Question"))

    content = models.CharField(max_length=1000,
                               blank=False,
                               help_text=_("Enter the answer text that "
                                           "you want displayed"),
                               verbose_name=_("Answer"))

    correct = models.BooleanField(blank=False,
                                  default=False,
                                  help_text=_("Is this a correct answer?"),
                                  verbose_name=_("Correct"))

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
