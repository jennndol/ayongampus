from django.conf.urls import url

from .views import QuizListView, QuizDetailView, QuizTake, export_scores_xls

urlpatterns = [
    url(r'^$', QuizListView.as_view(), name='quiz_index'),

    url(r'^export/xls/(?P<pk>[\d.]+)/$', export_scores_xls, name='export_scores_xls'),

    #  passes variable 'quiz_name' to quiz_take view
    url(r'^(?P<slug>[\w-]+)/$', QuizDetailView.as_view(), name='quiz_start_page'),

    url(r'^(?P<quiz_name>[\w-]+)/take/$', QuizTake.as_view(), name='quiz_question'),
]
