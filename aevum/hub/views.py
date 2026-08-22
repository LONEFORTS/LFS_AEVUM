from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from .forms import (
    AnnouncementForm, AssignmentForm, AttendanceForm, CodeSnippetForm,
    EventForm, FocusSessionForm, NoteForm, ProfileForm, RegisterForm,
    SubmissionForm, TagForm, TaskForm,
)
from .github_api import GitHubUploadError, upload_snippet_to_github
from .models import (
    Announcement, Assignment, AttendanceRecord, CodeSnippet, Event,
    FocusSession, Note, SharedLink, Submission, Tag, Task,
)


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        user.email = form.cleaned_data['email']
        user.save(update_fields=['email'])
        login(request, user)
        messages.success(request, 'Welcome to Aevum. Your premium student workspace is ready.')
        return redirect('dashboard')
    return render(request, 'registration/register.html', {'form': form})


def _streak_days(user):
    today = timezone.now().date()
    done_task_days = set(user.tasks.filter(status='done').values_list('updated_at__date', flat=True))
    focus_days = set(user.focus_sessions.values_list('completed_at__date', flat=True))
    attendance_days = set(user.attendance_records.filter(status='present').values_list('date', flat=True))
    days = done_task_days | focus_days | attendance_days
    if not days:
        return 0
    cursor = today if today in days else today - timedelta(days=1)
    streak = 0
    while cursor in days:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def _attendance_rate(user):
    total = user.attendance_records.count()
    if total == 0:
        return 0
    present = user.attendance_records.filter(status='present').count()
    return round((present / total) * 100)


@login_required
def dashboard(request):
    user = request.user
    tasks = user.tasks.all()
    notes = user.notes.all()
    snippets = user.snippets.all()
    assignments = user.assignments.all()
    events = user.events.order_by('start_date')[:6]
    announcements = user.announcements.all()[:5]
    recent_notes = notes[:5]
    recent_snippets = snippets[:5]
    due_assignments = assignments.order_by('due_date')[:5]
    stats = {
        'notes': notes.count(),
        'tasks_todo': tasks.filter(status='todo').count(),
        'tasks_doing': tasks.filter(status='doing').count(),
        'tasks_done': tasks.filter(status='done').count(),
        'events': user.events.count(),
        'assignments': assignments.count(),
        'attendance': user.attendance_records.count(),
        'announcements': user.announcements.count(),
        'snippets': snippets.count(),
        'github_uploaded': snippets.filter(github_uploaded=True).count(),
        'streak': _streak_days(user),
        'attendance_rate': _attendance_rate(user),
    }
    heatmap_days = []
    start = timezone.now().date() - timedelta(days=27)
    for i in range(28):
        d = start + timedelta(days=i)
        count = (
            user.focus_sessions.filter(completed_at__date=d).count()
            + user.tasks.filter(status='done', updated_at__date=d).count()
            + user.attendance_records.filter(date=d, status='present').count()
        )
        heatmap_days.append({'date': d, 'count': count, 'level': min(count, 4)})
    context = {
        'stats': stats,
        'recent_notes': recent_notes,
        'recent_snippets': recent_snippets,
        'events': events,
        'announcements': announcements,
        'due_assignments': due_assignments,
        'heatmap_days': heatmap_days,
    }
    return render(request, 'dashboard.html', context)


@login_required
def profile_settings(request):
    profile = request.user.profile
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile, branding, and GitHub settings updated successfully.')
        return redirect('profile')
    return render(request, 'profile.html', {'form': form, 'profile': profile})


@login_required
def search_view(request):
    query = request.GET.get('q', '').strip()
    notes = tasks = events = snippets = assignments = announcements = []
    if query:
        notes = request.user.notes.filter(Q(title__icontains=query) | Q(content__icontains=query))
        tasks = request.user.tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))
        events = request.user.events.filter(Q(title__icontains=query) | Q(description__icontains=query))
        snippets = request.user.snippets.filter(Q(title__icontains=query) | Q(content__icontains=query))
        assignments = request.user.assignments.filter(Q(title__icontains=query) | Q(course__icontains=query) | Q(instructions__icontains=query))
        announcements = request.user.announcements.filter(Q(title__icontains=query) | Q(content__icontains=query))
    return render(request, 'search.html', {
        'query': query,
        'notes': notes,
        'tasks': tasks,
        'events': events,
        'snippets': snippets,
        'assignments': assignments,
        'announcements': announcements,
    })


@login_required
def tag_create(request):
    form = TagForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        tag = form.save(commit=False)
        tag.user = request.user
        tag.save()
        messages.success(request, 'Tag created successfully.')
        return redirect('note-create')
    return render(request, 'simple_form.html', {'form': form, 'title': 'Create Tag'})


@login_required
def note_list(request):
    notes = request.user.notes.prefetch_related('tags').all()
    return render(request, 'notes/list.html', {'notes': notes})


@login_required
def note_create(request):
    form = NoteForm(request.POST or None, request.FILES or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        note = form.save(commit=False)
        note.user = request.user
        note.save()
        form.save_m2m()
        messages.success(request, 'Note saved successfully.')
        return redirect('note-detail', pk=note.pk)
    return render(request, 'notes/form.html', {'form': form, 'title': 'Create Note'})


@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note.objects.prefetch_related('tags'), pk=pk, user=request.user)
    return render(request, 'notes/detail.html', {'note': note})


@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    form = NoteForm(request.POST or None, request.FILES or None, instance=note, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Note updated successfully.')
        return redirect('note-detail', pk=note.pk)
    return render(request, 'notes/form.html', {'form': form, 'title': 'Edit Note'})


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully.')
        return redirect('note-list')
    return render(request, 'confirm_delete.html', {'title': 'Delete Note', 'object_name': note.title})


@login_required
def task_board(request):
    tasks = request.user.tasks.all()
    return render(request, 'tasks/board.html', {
        'todo_tasks': tasks.filter(status='todo'),
        'doing_tasks': tasks.filter(status='doing'),
        'done_tasks': tasks.filter(status='done'),
    })


@login_required
def task_create(request):
    form = TaskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        messages.success(request, 'Task created successfully.')
        return redirect('task-board')
    return render(request, 'tasks/form.html', {'form': form, 'title': 'Create Task'})


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Task updated successfully.')
        return redirect('task-board')
    return render(request, 'tasks/form.html', {'form': form, 'title': 'Edit Task'})


@login_required
def task_move(request, pk, status):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if status in {'todo', 'doing', 'done'}:
        task.status = status
        task.save(update_fields=['status', 'updated_at'])
        messages.success(request, f'Task moved to {status}.')
    return redirect('task-board')


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('task-board')
    return render(request, 'confirm_delete.html', {'title': 'Delete Task', 'object_name': task.title})


@login_required
def event_calendar(request):
    events = request.user.events.all()
    return render(request, 'events/calendar.html', {'events': events})


@login_required
def event_create(request):
    form = EventForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        event = form.save(commit=False)
        event.user = request.user
        event.save()
        messages.success(request, 'Event created successfully.')
        return redirect('event-calendar')
    return render(request, 'events/form.html', {'form': form, 'title': 'Create Event'})


@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    form = EventForm(request.POST or None, instance=event)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Event updated successfully.')
        return redirect('event-calendar')
    return render(request, 'events/form.html', {'form': form, 'title': 'Edit Event'})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('event-calendar')
    return render(request, 'confirm_delete.html', {'title': 'Delete Event', 'object_name': event.title})


@login_required
def assignment_list(request):
    assignments = request.user.assignments.all()
    return render(request, 'assignments/list.html', {'assignments': assignments})


@login_required
def assignment_create(request):
    form = AssignmentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        assignment = form.save(commit=False)
        assignment.user = request.user
        assignment.save()
        messages.success(request, 'Assignment created successfully.')
        return redirect('assignment-detail', pk=assignment.pk)
    return render(request, 'assignments/form.html', {'form': form, 'title': 'Create Assignment'})


@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    submissions = assignment.submissions.filter(user=request.user)
    submission_form = SubmissionForm()
    return render(request, 'assignments/detail.html', {
        'assignment': assignment,
        'submissions': submissions,
        'submission_form': submission_form,
    })


@login_required
def assignment_update(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    form = AssignmentForm(request.POST or None, request.FILES or None, instance=assignment)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Assignment updated successfully.')
        return redirect('assignment-detail', pk=assignment.pk)
    return render(request, 'assignments/form.html', {'form': form, 'title': 'Edit Assignment'})


@login_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Assignment deleted successfully.')
        return redirect('assignment-list')
    return render(request, 'confirm_delete.html', {'title': 'Delete Assignment', 'object_name': assignment.title})


@login_required
def submission_create(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    form = SubmissionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        submission = form.save(commit=False)
        submission.user = request.user
        submission.assignment = assignment
        submission.save()
        if submission.status == 'submitted':
            assignment.status = 'submitted'
            assignment.save(update_fields=['status'])
        messages.success(request, 'Submission saved successfully.')
        return redirect('assignment-detail', pk=assignment.pk)
    return render(request, 'assignments/submission_form.html', {'form': form, 'assignment': assignment})


@login_required
def attendance_list(request):
    records = request.user.attendance_records.all()
    form = AttendanceForm(initial={'date': timezone.now().date()})
    return render(request, 'attendance/list.html', {'records': records, 'form': form})


@login_required
def attendance_create(request):
    form = AttendanceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        record = form.save(commit=False)
        record.user = request.user
        record.save()
        messages.success(request, 'Attendance logged successfully.')
    else:
        messages.error(request, 'Attendance could not be saved. The date may already exist.')
    return redirect('attendance-list')


@login_required
def announcement_list(request):
    announcements = request.user.announcements.all()
    return render(request, 'announcements/list.html', {'announcements': announcements})


@login_required
def announcement_create(request):
    form = AnnouncementForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        announcement = form.save(commit=False)
        announcement.user = request.user
        announcement.save()
        messages.success(request, 'Announcement created successfully.')
        return redirect('announcement-list')
    return render(request, 'announcements/form.html', {'form': form, 'title': 'Create Announcement'})


@login_required
def announcement_update(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk, user=request.user)
    form = AnnouncementForm(request.POST or None, instance=announcement)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Announcement updated successfully.')
        return redirect('announcement-list')
    return render(request, 'announcements/form.html', {'form': form, 'title': 'Edit Announcement'})


@login_required
def announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk, user=request.user)
    if request.method == 'POST':
        announcement.delete()
        messages.success(request, 'Announcement deleted successfully.')
        return redirect('announcement-list')
    return render(request, 'confirm_delete.html', {'title': 'Delete Announcement', 'object_name': announcement.title})


@login_required
def snippet_list(request):
    snippets = request.user.snippets.all()
    return render(request, 'snippets/list.html', {'snippets': snippets})


@login_required
def snippet_create(request):
    form = CodeSnippetForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        snippet = form.save(commit=False)
        snippet.user = request.user
        snippet.save()
        messages.success(request, 'Code snippet saved successfully.')
        return redirect('snippet-detail', pk=snippet.pk)
    return render(request, 'snippets/form.html', {'form': form, 'title': 'Create Code Snippet'})


@login_required
def snippet_detail(request, pk):
    snippet = get_object_or_404(CodeSnippet, pk=pk, user=request.user)
    return render(request, 'snippets/detail.html', {'snippet': snippet})


@login_required
def snippet_update(request, pk):
    snippet = get_object_or_404(CodeSnippet, pk=pk, user=request.user)
    form = CodeSnippetForm(request.POST or None, request.FILES or None, instance=snippet)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Code snippet updated successfully.')
        return redirect('snippet-detail', pk=snippet.pk)
    return render(request, 'snippets/form.html', {'form': form, 'title': 'Edit Code Snippet'})


@login_required
def snippet_delete(request, pk):
    snippet = get_object_or_404(CodeSnippet, pk=pk, user=request.user)
    if request.method == 'POST':
        snippet.delete()
        messages.success(request, 'Code snippet deleted successfully.')
        return redirect('snippet-list')
    return render(request, 'confirm_delete.html', {'title': 'Delete Code Snippet', 'object_name': snippet.title})


@login_required
def snippet_publish_github(request, pk):
    snippet = get_object_or_404(CodeSnippet, pk=pk, user=request.user)
    try:
        url = upload_snippet_to_github(request.user.profile, snippet)
        messages.success(request, f'Code uploaded to GitHub successfully: {url}')
    except GitHubUploadError as exc:
        messages.error(request, str(exc))
    return redirect('snippet-detail', pk=snippet.pk)


@login_required
def focus_timer(request):
    form = FocusSessionForm(initial={'minutes': 25, 'productivity_score': 5})
    sessions = request.user.focus_sessions.all()[:10]
    return render(request, 'focus/timer.html', {'form': form, 'sessions': sessions})


@login_required
def focus_log(request):
    if request.method != 'POST':
        return redirect('focus-timer')
    form = FocusSessionForm(request.POST)
    if form.is_valid():
        session = form.save(commit=False)
        session.user = request.user
        session.save()
        messages.success(request, 'Focus session logged successfully.')
    else:
        messages.error(request, 'Could not log the focus session. Check the values and try again.')
    return redirect('focus-timer')


def _create_or_get_share(user, target_type, note=None, snippet=None, assignment=None):
    obj, _ = SharedLink.objects.get_or_create(user=user, target_type=target_type, note=note, snippet=snippet, assignment=assignment)
    return obj


@login_required
def share_profile(request):
    share = _create_or_get_share(request.user, 'profile')
    return render(request, 'share/settings.html', {'share': share, 'share_url': request.build_absolute_uri(reverse('public-share', args=[share.slug]))})


@login_required
def share_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    share = _create_or_get_share(request.user, 'note', note=note)
    return render(request, 'share/settings.html', {'share': share, 'share_url': request.build_absolute_uri(reverse('public-share', args=[share.slug]))})


@login_required
def share_snippet(request, pk):
    snippet = get_object_or_404(CodeSnippet, pk=pk, user=request.user)
    share = _create_or_get_share(request.user, 'snippet', snippet=snippet)
    return render(request, 'share/settings.html', {'share': share, 'share_url': request.build_absolute_uri(reverse('public-share', args=[share.slug]))})


@login_required
def share_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk, user=request.user)
    share = _create_or_get_share(request.user, 'assignment', assignment=assignment)
    return render(request, 'share/settings.html', {'share': share, 'share_url': request.build_absolute_uri(reverse('public-share', args=[share.slug]))})


def public_share(request, slug):
    share = get_object_or_404(SharedLink, slug=slug)
    if share.target_type == 'profile':
        return render(request, 'share/profile.html', {'profile': share.user.profile, 'user_obj': share.user})
    if share.target_type == 'note' and share.note:
        return render(request, 'share/public.html', {'title': share.note.title, 'body_html': share.note.rendered_content, 'kind': 'Shared Note'})
    if share.target_type == 'snippet' and share.snippet:
        return render(request, 'share/public.html', {'title': share.snippet.title, 'body_html': f'<pre>{share.snippet.display_content}</pre>', 'kind': 'Shared Code Snippet'})
    if share.target_type == 'assignment' and share.assignment:
        body_html = f"<p><strong>Course:</strong> {share.assignment.course}</p><p><strong>Due date:</strong> {share.assignment.due_date}</p><div><strong>Instructions:</strong><br>{share.assignment.instructions}</div>"
        return render(request, 'share/public.html', {'title': share.assignment.title, 'body_html': body_html, 'kind': 'Shared Assignment'})
    raise Http404('Shared item not found.')
