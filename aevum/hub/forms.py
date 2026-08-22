from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    Announcement, Assignment, AttendanceRecord, CodeSnippet, Event,
    FocusSession, Note, Profile, Submission, Tag, Task
)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'full_name', 'course', 'year_level', 'phone', 'bio', 'portfolio_headline',
            'avatar', 'github_username', 'github_repo', 'github_branch', 'github_token', 'accent_color'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'github_token': forms.PasswordInput(render_value=True),
            'accent_color': forms.TextInput(attrs={'type': 'color'}),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'color']
        widgets = {'color': forms.TextInput(attrs={'type': 'color'})}


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'attachment', 'is_pinned', 'is_public', 'tags']
        widgets = {'content': forms.Textarea(attrs={'rows': 12}), 'tags': forms.CheckboxSelectMultiple()}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['tags'].queryset = Tag.objects.filter(user=user)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']
        widgets = {'description': forms.Textarea(attrs={'rows': 4}), 'due_date': forms.DateInput(attrs={'type': 'date'})}


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'end_date', 'color', 'is_public']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'color': forms.TextInput(attrs={'type': 'color'}),
        }


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'course', 'instructions', 'due_date', 'status', 'priority', 'attachment', 'github_required', 'is_public']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 6}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['title', 'notes', 'github_link', 'submitted_file', 'status']
        widgets = {'notes': forms.Textarea(attrs={'rows': 5})}


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['date', 'status', 'note']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'is_pinned', 'is_public']
        widgets = {'content': forms.Textarea(attrs={'rows': 5})}


class CodeSnippetForm(forms.ModelForm):
    class Meta:
        model = CodeSnippet
        fields = ['title', 'language', 'content', 'code_file', 'is_public']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 14, 'placeholder': 'Paste your code here if you do not want to upload a file.'}),
        }


class FocusSessionForm(forms.ModelForm):
    class Meta:
        model = FocusSession
        fields = ['minutes', 'note', 'productivity_score']
