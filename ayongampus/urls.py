"""ayongampus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from ayongampus import settings
from ayongampus.activities import views as activities_views
from ayongampus.authentication import views as ayongampus_auth_views
from ayongampus.core import views as core_views
from ayongampus.quiz.essay.views import EssayQuestionCreateView, EssayQuestionUpdateView
from ayongampus.quiz.multichoice.views import MCQuestionAnswerCreate, MCQuestionAnswerUpdate
from ayongampus.quiz.truefalse.views import TFQuestionCreateView, TFQuestionUpdateView
from ayongampus.quiz.views import quiz_list, quiz_create, quiz_update, quiz_delete, quiz_detail, QuizQuestionCreateView, \
    remove_question_from_quiz, QuestionListView, QuestionDeleteView, QuizUserProgressView, QuizMarkingList, \
    QuizMarkingDetail
from ayongampus.search import views as search_views
from ayongampus.subject.views import SubjectChapterCreate, SubjectChapterUpdate, SubjectListView, SubjectDeleteView, \
    ChapterAutocomplete, overview
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^4dm1n/', admin.site.urls),
    url(r'^quiz/', include('ayongampus.quiz.urls')),

    url(r'^progress/$', QuizUserProgressView.as_view(), name='quiz_progress'),

    url(r'^dashboard/$', overview, name='core_overview'),

    url(r'^dashboard/quizzes/$', quiz_list, name='core_quiz_list'),
    url(r'^dashboard/quizzes/create/$', quiz_create, name='core_quiz_create'),
    url(r'^dashboard/quizzes/(?P<pk>\d+)/update/$', quiz_update, name='core_quiz_update'),
    url(r'^dashboard/quizzes/(?P<pk>\d+)/delete/$', quiz_delete, name='core_quiz_delete'),
    url(r'^dashboard/quizzes/(?P<slug>[\w-]+)/$', quiz_detail, name='core_quiz_detail'),

    url(r'^dashboard/quizzes/(?P<pk>\d+)/q/$', QuizQuestionCreateView.as_view(), name='core_question_add'),
    url(r'^dashboard/quizzes/(?P<pk_quiz>[0-9]+)/delete/(?P<pk_question>[0-9]+)/$', remove_question_from_quiz,
        name='core_remove_question_from_quiz'),

    url(r'^dashboard/chapter-autocomplete/$', ChapterAutocomplete.as_view(), name='chapter-autocomplete', ),

    url(r'dashboard/subjects/$', SubjectListView.as_view(), name='core_subject_list'),
    url(r'dashboard/subjects/add/$', SubjectChapterCreate.as_view(), name='core_subject_add'),
    url(r'dashboard/subjects/(?P<pk>[0-9]+)/update/$', SubjectChapterUpdate.as_view(), name='core_subject_update'),
    url(r'dashboard/subjects/(?P<pk>[0-9]+)/delete/$', SubjectDeleteView.as_view(), name='core_subject_delete'),

    url(r'^dashboard/questions/mcq/$', MCQuestionAnswerCreate.as_view(), name='core_mcquestion_add'),
    url(r'^dashboard/questions/mcq/(?P<pk>[0-9]+)/$', MCQuestionAnswerUpdate.as_view(),
        name='core_mcquestion_update'),

    url(r'^dashboard/questions/$', QuestionListView.as_view(), name='core_question_list'),
    url(r'^dashboard/questions/(?P<pk>[0-9]+)/delete/$', QuestionDeleteView.as_view(), name='core_question_delete'),
    url(r'^dashboard/questions/tfq/$', TFQuestionCreateView.as_view(), name='core_tfquestion_add'),
    url(r'^dashboard/questions/tfq/(?P<pk>[0-9]+)/update/$', TFQuestionUpdateView.as_view(),
        name='core_tfquestion_update'),

    url(r'^dashboard/questions/essay/$', EssayQuestionCreateView.as_view(), name='core_essay_add'),
    url(r'^dashboard/questions/essay/(?P<pk>[0-9]+)/update/$', EssayQuestionUpdateView.as_view(),
        name='core_essay_update'),
    url(r'^', include('password_reset.urls')),

    url(r'^dashboard/marking/$', QuizMarkingList.as_view(), name='core_quiz_marking'),
    url(r'^dashboard/marking/(?P<pk>[\d.]+)/$', QuizMarkingDetail.as_view(), name='core_quiz_marking_detail'),

    # bootcamp
    url(r'^$', core_views.home, name='home'),
    url(r'^login', auth_views.login, {'template_name': 'core/cover.html'},
        name='login'),
    url(r'^logout', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', ayongampus_auth_views.signup, name='signup'),
    url(r'^settings/$', core_views.settings, name='settings'),
    url(r'^settings/picture/$', core_views.picture, name='picture'),
    url(r'^settings/upload_picture/$', core_views.upload_picture,
        name='upload_picture'),
    url(r'^settings/save_uploaded_picture/$', core_views.save_uploaded_picture,
        name='save_uploaded_picture'),
    url(r'^settings/password/$', core_views.password, name='password'),

    url(r'^feeds/', include('ayongampus.feeds.urls')),
    url(r'^questions/', include('ayongampus.questions.urls')),
    url(r'^articles/', include('ayongampus.articles.urls')),
    url(r'^messages/', include('ayongampus.messenger.urls')),
    url(r'^notifications/$', activities_views.notifications,
        name='notifications'),
    url(r'^notifications/last/$', activities_views.last_notifications,
        name='last_notifications'),
    url(r'^notifications/check/$', activities_views.check_notifications,
        name='check_notifications'),
    url(r'^search/$', search_views.search, name='search'),
    url(r'^quiz/', include('ayongampus.quiz.urls')),
    url(r'^members/', include('follow.urls')),

    url(r'^i18n/', include('django.conf.urls.i18n', namespace='i18n')),

    url(r'^(?P<username>[^/]+)/$', core_views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Ayongampus Administration'