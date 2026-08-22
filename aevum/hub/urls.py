from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_settings, name='profile'),
    path('search/', views.search_view, name='search'),

    path('tags/new/', views.tag_create, name='tag-create'),

    path('notes/', views.note_list, name='note-list'),
    path('notes/new/', views.note_create, name='note-create'),
    path('notes/<int:pk>/', views.note_detail, name='note-detail'),
    path('notes/<int:pk>/edit/', views.note_update, name='note-update'),
    path('notes/<int:pk>/delete/', views.note_delete, name='note-delete'),

    path('tasks/', views.task_board, name='task-board'),
    path('tasks/new/', views.task_create, name='task-create'),
    path('tasks/<int:pk>/edit/', views.task_update, name='task-update'),
    path('tasks/<int:pk>/move/<str:status>/', views.task_move, name='task-move'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task-delete'),

    path('events/', views.event_calendar, name='event-calendar'),
    path('events/new/', views.event_create, name='event-create'),
    path('events/<int:pk>/edit/', views.event_update, name='event-update'),
    path('events/<int:pk>/delete/', views.event_delete, name='event-delete'),

    path('assignments/', views.assignment_list, name='assignment-list'),
    path('assignments/new/', views.assignment_create, name='assignment-create'),
    path('assignments/<int:pk>/', views.assignment_detail, name='assignment-detail'),
    path('assignments/<int:pk>/edit/', views.assignment_update, name='assignment-update'),
    path('assignments/<int:pk>/delete/', views.assignment_delete, name='assignment-delete'),
    path('assignments/<int:pk>/submit/', views.submission_create, name='submission-create'),

    path('attendance/', views.attendance_list, name='attendance-list'),
    path('attendance/log/', views.attendance_create, name='attendance-create'),

    path('announcements/', views.announcement_list, name='announcement-list'),
    path('announcements/new/', views.announcement_create, name='announcement-create'),
    path('announcements/<int:pk>/edit/', views.announcement_update, name='announcement-update'),
    path('announcements/<int:pk>/delete/', views.announcement_delete, name='announcement-delete'),

    path('snippets/', views.snippet_list, name='snippet-list'),
    path('snippets/new/', views.snippet_create, name='snippet-create'),
    path('snippets/<int:pk>/', views.snippet_detail, name='snippet-detail'),
    path('snippets/<int:pk>/edit/', views.snippet_update, name='snippet-update'),
    path('snippets/<int:pk>/delete/', views.snippet_delete, name='snippet-delete'),
    path('snippets/<int:pk>/publish/', views.snippet_publish_github, name='snippet-publish'),

    path('focus/', views.focus_timer, name='focus-timer'),
    path('focus/log/', views.focus_log, name='focus-log'),

    path('share/profile/', views.share_profile, name='share-profile'),
    path('share/note/<int:pk>/', views.share_note, name='share-note'),
    path('share/snippet/<int:pk>/', views.share_snippet, name='share-snippet'),
    path('share/assignment/<int:pk>/', views.share_assignment, name='share-assignment'),
    path('s/<slug:slug>/', views.public_share, name='public-share'),
]
