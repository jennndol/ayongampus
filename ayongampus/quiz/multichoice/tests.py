from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db.models.fields.files import ImageFieldFile
from django.test import TestCase
from django.utils.six import StringIO

from ayongampus.quiz.quiz_types import is_list, answer_list_validation
from .models import MCQuestion, Answer


class TestMCQuestionModel(TestCase):
    def setUp(self):
        self.u = User.objects.create(id=100, username="John", is_active=True, is_staff=True)
        self.q = MCQuestion.objects.create(id=1,
                                           content=("WHAT is the airspeed" +
                                                    "velocity of an unladen" +
                                                    "swallow?"),
                                           explanation="I, I don't know that!",
                                           author=self.u)

        self.answer1 = Answer.objects.create(id=123,
                                             question=self.q,
                                             content="African",
                                             correct=False)

        self.answer2 = Answer.objects.create(id=456,
                                             question=self.q,
                                             content="European",
                                             correct=True)

    def test_answers(self):
        answers = Answer.objects.filter(question=self.q)
        correct_a = Answer.objects.get(question=self.q,
                                       correct=True)
        answers_by_method = self.q.get_answers()

        self.assertEqual(answers.count(), 2)
        self.assertEqual(correct_a.content, "European")

        if is_list(123):
            pass
        else:
            self.assertEqual(self.q.check_if_correct(123), False)
            self.assertEqual(self.q.check_if_correct(456), True)
            self.assertEqual(answers_by_method.count(), 2)
            self.assertEqual(self.q.answer_choice_to_string(123),
                             self.answer1.content)

    def test_figure(self):
        # http://stackoverflow.com/a/2473445/1694979
        imgfile = StringIO(
            'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,'
            '\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
        imgfile.name = 'test_img_file.gif'

        self.q.figure.save('image', ContentFile(imgfile.read()))
        self.assertIsInstance(self.q.figure, ImageFieldFile)

    def test_answer_to_string(self):
        if is_list(123):
            pass
        else:
            self.assertEqual('African', self.q.answer_choice_to_string(123))

    def test_is_list(self):
        self.assertEqual(True, is_list([1, 2, 3]))

    def test_answer_list_validation(self):
        self.assertEqual(True, answer_list_validation([1, 2, 3], [2, 1, 3]))

    def tearDown(self):
        self.q.delete()
        self.u.delete()
        self.answer1.delete()
        self.answer2.delete()
