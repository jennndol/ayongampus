# -*- coding: iso-8859-15 -*-

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Subject, Chapter, get_subject_by_subject_name, get_subject_by_id


class TestSubject(TestCase):
    def setUp(self):
        self.u = User.objects.create(id=100, username="John", is_active=True, is_staff=True)

        self.c1 = Subject.objects.create(id=100, subject='squishy-berries', author=self.u)

        self.sub1 = Chapter.objects.create(chapter='Red',
                                           subject=self.c1, author=self.u)

    def test_subjects(self):
        self.assertEqual(self.c1.subject, 'squishy-berries')

    def test_chapter(self):
        self.assertEqual(self.sub1.subject, self.c1)

    def test_get_subject_by_subject_name(self):
        self.assertEqual(get_subject_by_subject_name('squishy-berries').subject, 'squishy-berries')

    def test_get_subject_by_id(self):
        self.assertEqual(get_subject_by_id(100).subject, 'squishy-berries')

    def tearDown(self):
        self.sub1.delete()
        self.c1.delete()
        self.u.delete()
