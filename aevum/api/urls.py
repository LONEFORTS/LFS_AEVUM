from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    AnnouncementViewSet, AssignmentViewSet, AttendanceViewSet,
    CodeSnippetViewSet, EventViewSet, NoteViewSet, StatsAPIView,
    SubmissionViewSet, TagViewSet, TaskViewSet,
)

router = DefaultRouter()
router.register('tags', TagViewSet, basename='api-tags')
router.register('notes', NoteViewSet, basename='api-notes')
router.register('tasks', TaskViewSet, basename='api-tasks')
router.register('events', EventViewSet, basename='api-events')
router.register('assignments', AssignmentViewSet, basename='api-assignments')
router.register('submissions', SubmissionViewSet, basename='api-submissions')
router.register('attendance', AttendanceViewSet, basename='api-attendance')
router.register('announcements', AnnouncementViewSet, basename='api-announcements')
router.register('snippets', CodeSnippetViewSet, basename='api-snippets')

urlpatterns = [
    path('stats/', StatsAPIView.as_view(), name='api-stats'),
    path('', include(router.urls)),
]
