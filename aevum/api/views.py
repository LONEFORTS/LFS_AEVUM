from rest_framework import permissions, response, viewsets, views
from hub.models import Announcement, Assignment, AttendanceRecord, CodeSnippet, Event, Note, Submission, Tag, Task
from .serializers import (
    AnnouncementSerializer, AssignmentSerializer, AttendanceSerializer,
    CodeSnippetSerializer, EventSerializer, NoteSerializer,
    SubmissionSerializer, TagSerializer, TaskSerializer,
)


class UserFilteredQuerySetMixin:
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(UserFilteredQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Tag.objects.all()
    search_fields = ['name']


class NoteViewSet(UserFilteredQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Note.objects.prefetch_related('tags').all()
    search_fields = ['title', 'content']


class TaskViewSet(UserFilteredQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()
    filterset_fields = ['status', 'priority']
    search_fields = ['title', 'description']


class EventViewSet(UserFilteredQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Event.objects.all()
    search_fields = ['title', 'description']


class AssignmentViewSet(UserFilteredQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Assignment.objects.all()
    filterset_fields = ['status', 'priority', 'github_required']
    search_fields = ['title', 'course', 'instructions']


class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Submission.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AttendanceViewSet(UserFilteredQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = AttendanceRecord.objects.all()
    filterset_fields = ['status']


class AnnouncementViewSet(UserFilteredQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Announcement.objects.all()
    search_fields = ['title', 'content']


class CodeSnippetViewSet(UserFilteredQuerySetMixin, viewsets.ModelViewSet):
    serializer_class = CodeSnippetSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = CodeSnippet.objects.all()
    filterset_fields = ['language', 'is_public', 'github_uploaded']
    search_fields = ['title', 'content']


class StatsAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'notes': Note.objects.filter(user=user).count(),
            'tasks_todo': Task.objects.filter(user=user, status='todo').count(),
            'tasks_doing': Task.objects.filter(user=user, status='doing').count(),
            'tasks_done': Task.objects.filter(user=user, status='done').count(),
            'events': Event.objects.filter(user=user).count(),
            'assignments': Assignment.objects.filter(user=user).count(),
            'attendance': AttendanceRecord.objects.filter(user=user).count(),
            'announcements': Announcement.objects.filter(user=user).count(),
            'snippets': CodeSnippet.objects.filter(user=user).count(),
            'github_uploaded': CodeSnippet.objects.filter(user=user, github_uploaded=True).count(),
        }
        return response.Response(data)
