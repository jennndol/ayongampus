from django.conf.urls import url

from .views import SubjectsListView, ViewQuizListBySubject

urlpatterns = [
    url(r'^$', SubjectsListView.as_view(), name='quiz_subject_list_all'),
    url(r'^(?P<subject_name>[\w|\W-]+)/$', ViewQuizListBySubject.as_view(),
        name='quiz_subject_list_matching'),
]
