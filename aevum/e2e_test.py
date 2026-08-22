import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aevum.settings')
import django
django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from hub.models import Announcement, Assignment, AttendanceRecord, CodeSnippet, Event, FocusSession, Note, SharedLink, Submission, Tag, Task


def ok(name, condition):
    if not condition:
        raise AssertionError(name)
    print(f'PASS: {name}')


def main():
    settings.ALLOWED_HOSTS = ['testserver', 'localhost', '127.0.0.1']
    User.objects.all().delete()
    client = Client()

    response = client.post('/register/', {
        'username': 'student1',
        'email': 'student1@example.com',
        'password1': 'StrongPass123!',
        'password2': 'StrongPass123!',
    }, follow=True)
    ok('register redirects to dashboard', response.status_code == 200 and b'student1' in response.content and b'Welcome' in response.content)

    response = client.post('/tags/new/', {'name': 'Math', 'color': '#ff0000'}, follow=True)
    ok('create tag', response.status_code == 200 and Tag.objects.filter(user__username='student1', name='Math').exists())
    tag = Tag.objects.get(name='Math')

    note_file = SimpleUploadedFile('note.txt', b'attachment text', content_type='text/plain')
    response = client.post('/notes/new/', {
        'title': 'Calculus Chapter 5',
        'content': '# Math Notes\nDerivative rules',
        'attachment': note_file,
        'is_pinned': 'on',
        'is_public': 'on',
        'tags': [str(tag.pk)],
    }, follow=True)
    ok('create note', response.status_code == 200 and b'Calculus Chapter 5' in response.content and b'Download attached file' in response.content)
    note = Note.objects.get(title='Calculus Chapter 5')
    ok('note pinned', note.is_pinned)
    ok('note public', note.is_public)

    response = client.post('/tasks/new/', {
        'title': 'Finish capstone report',
        'description': 'Write testing chapter',
        'status': 'todo',
        'priority': 'high',
        'due_date': '2026-08-20',
    }, follow=True)
    ok('create task', response.status_code == 200 and Task.objects.filter(title='Finish capstone report').exists())
    task = Task.objects.get(title='Finish capstone report')

    response = client.get(f'/tasks/{task.pk}/move/doing/', follow=True)
    task.refresh_from_db()
    ok('task move to doing', task.status == 'doing')

    response = client.post('/events/new/', {
        'title': 'Math Midterm',
        'description': 'Exam preparation',
        'start_date': '2026-08-25',
        'end_date': '2026-08-25',
        'color': '#00ffcc',
        'is_public': 'on',
    }, follow=True)
    ok('create event', response.status_code == 200 and Event.objects.filter(title='Math Midterm').exists())

    assignment_file = SimpleUploadedFile('brief.txt', b'Capstone brief', content_type='text/plain')
    response = client.post('/assignments/new/', {
        'title': 'Capstone Module',
        'course': 'Software Engineering',
        'instructions': 'Upload project files and GitHub link.',
        'due_date': '2026-08-28',
        'status': 'open',
        'priority': 'high',
        'attachment': assignment_file,
        'github_required': 'on',
        'is_public': 'on',
    }, follow=True)
    ok('create assignment', response.status_code == 200 and Assignment.objects.filter(title='Capstone Module').exists())
    assignment = Assignment.objects.get(title='Capstone Module')

    submission_file = SimpleUploadedFile('submission.txt', b'my final submission', content_type='text/plain')
    response = client.post(f'/assignments/{assignment.pk}/submit/', {
        'title': 'Final Submission',
        'notes': 'Submitted from Aevum',
        'github_link': 'https://github.com/example/repo',
        'submitted_file': submission_file,
        'status': 'submitted',
    }, follow=True)
    ok('create submission', response.status_code == 200 and Submission.objects.filter(title='Final Submission').exists())

    response = client.post('/attendance/log/', {
        'date': '2026-08-19',
        'status': 'present',
        'note': 'Attended class',
    }, follow=True)
    ok('create attendance', response.status_code == 200 and AttendanceRecord.objects.filter(note='Attended class').exists())

    response = client.post('/announcements/new/', {
        'title': 'Project Review',
        'content': 'Capstone review this Friday',
        'is_pinned': 'on',
        'is_public': 'on',
    }, follow=True)
    ok('create announcement', response.status_code == 200 and Announcement.objects.filter(title='Project Review').exists())

    code_file = SimpleUploadedFile('hello.py', b'print("hello aevum")\n', content_type='text/x-python')
    response = client.post('/snippets/new/', {
        'title': 'Hello Script',
        'language': 'python',
        'content': 'print("hello aevum")',
        'code_file': code_file,
        'is_public': 'on',
    }, follow=True)
    ok('create snippet', response.status_code == 200 and CodeSnippet.objects.filter(title='Hello Script').exists())
    snippet = CodeSnippet.objects.get(title='Hello Script')
    ok('snippet detail shows code', b'hello aevum' in response.content)

    response = client.get(f'/snippets/{snippet.pk}/publish/', follow=True)
    ok('github publish friendly error without config', b'GitHub token and repository are required' in response.content)

    response = client.post('/focus/log/', {'minutes': 25, 'note': 'Study session', 'productivity_score': 8}, follow=True)
    ok('focus session logged', response.status_code == 200 and FocusSession.objects.filter(note='Study session').exists())

    response = client.get('/search/?q=capstone')
    ok('search finds assignment or announcement', b'Capstone Module' in response.content or b'Project Review' in response.content)

    response = client.get('/dashboard/')
    ok('dashboard renders', response.status_code == 200 and b'Consistency' in response.content and b'Academic activity' in response.content and b'assignments' in response.content)

    response = client.get('/share/profile/')
    ok('share profile page ready', response.status_code == 200 and b'Your public link is ready' in response.content)
    share = SharedLink.objects.filter(user__username='student1', target_type='profile').first()
    ok('share object exists', share is not None)

    anon = Client()
    response = anon.get(f'/s/{share.slug}/')
    ok('public profile opens without login', response.status_code == 200 and b'student1' in response.content)

    response = client.get('/api/stats/')
    ok('api stats endpoint', response.status_code == 200 and response.json()['notes'] == 1 and response.json()['snippets'] == 1 and response.json()['assignments'] == 1)

    response = client.get('/api/notes/')
    ok('api notes list', response.status_code == 200 and len(response.json()) == 1)

    response = client.get('/api/assignments/')
    ok('api assignments list', response.status_code == 200 and len(response.json()) == 1)

    other = User.objects.create_user(username='student2', password='StrongPass123!')
    other_client = Client()
    other_client.login(username='student2', password='StrongPass123!')
    response = other_client.get(f'/notes/{note.pk}/')
    ok('cross user note blocked', response.status_code == 404)

    response = client.get('/logout/', follow=True)
    ok('logout works', response.status_code == 200)
    print('\nALL TESTS PASSED')


if __name__ == '__main__':
    main()
