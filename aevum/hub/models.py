import uuid
import markdown
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150, blank=True)
    course = models.CharField(max_length=120, blank=True)
    year_level = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    portfolio_headline = models.CharField(max_length=180, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    github_username = models.CharField(max_length=120, blank=True)
    github_repo = models.CharField(max_length=180, blank=True)
    github_branch = models.CharField(max_length=80, default='main', blank=True)
    github_token = models.CharField(max_length=255, blank=True)
    accent_color = models.CharField(max_length=20, default='#1d9bf0', blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"


class Tag(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='#1d9bf0')

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['name']

    def __str__(self):
        return self.name


class Note(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    attachment = models.FileField(upload_to='notes/', blank=True, null=True)
    is_pinned = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, blank=True, related_name='notes')

    class Meta:
        ordering = ['-is_pinned', '-updated_at']

    def __str__(self):
        return self.title

    @property
    def rendered_content(self):
        html = markdown.markdown(self.content, extensions=['fenced_code', 'tables'])
        return mark_safe(html)


class Task(TimeStampedModel):
    STATUS_CHOICES = [('todo', 'To Do'), ('doing', 'Doing'), ('done', 'Done')]
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['status', '-created_at']

    def __str__(self):
        return self.title


class Event(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    color = models.CharField(max_length=20, default='#1d9bf0')
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_date', 'title']

    def __str__(self):
        return self.title


class Assignment(TimeStampedModel):
    STATUS_CHOICES = [('open', 'Open'), ('submitted', 'Submitted'), ('reviewed', 'Reviewed'), ('closed', 'Closed')]
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    course = models.CharField(max_length=120)
    instructions = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    attachment = models.FileField(upload_to='assignment_files/', blank=True, null=True)
    github_required = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['due_date', '-created_at']

    def __str__(self):
        return self.title


class Submission(TimeStampedModel):
    STATUS_CHOICES = [('draft', 'Draft'), ('submitted', 'Submitted'), ('accepted', 'Accepted')]
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    github_link = models.URLField(blank=True)
    submitted_file = models.FileField(upload_to='submission_files/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.assignment.title} - {self.user.username}"


class AttendanceRecord(TimeStampedModel):
    STATUS_CHOICES = [('present', 'Present'), ('absent', 'Absent'), ('late', 'Late'), ('leave', 'Leave')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    note = models.CharField(max_length=180, blank=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.date}"


class Announcement(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_pinned = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return self.title


class CodeSnippet(TimeStampedModel):
    LANGUAGE_CHOICES = [
        ('python', 'Python'), ('javascript', 'JavaScript'), ('html', 'HTML'), ('css', 'CSS'),
        ('java', 'Java'), ('cpp', 'C++'), ('c', 'C'), ('php', 'PHP'), ('sql', 'SQL'), ('text', 'Text')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippets')
    title = models.CharField(max_length=200)
    language = models.CharField(max_length=30, choices=LANGUAGE_CHOICES, default='python')
    content = models.TextField(blank=True)
    code_file = models.FileField(
        upload_to='code_uploads/', blank=True, null=True,
        validators=[FileExtensionValidator(allowed_extensions=['py', 'js', 'html', 'css', 'java', 'cpp', 'c', 'php', 'txt', 'sql', 'json', 'md'])],
    )
    is_public = models.BooleanField(default=False)
    github_uploaded = models.BooleanField(default=False)
    github_url = models.URLField(blank=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title

    @property
    def display_content(self):
        if self.content:
            return self.content
        if self.code_file:
            try:
                self.code_file.open('rb')
                data = self.code_file.read().decode('utf-8', errors='replace')
                self.code_file.close()
                return data
            except Exception:
                return ''
        return ''


class FocusSession(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='focus_sessions')
    minutes = models.PositiveIntegerField(default=25)
    note = models.CharField(max_length=180, blank=True)
    productivity_score = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(10)])
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']


class SharedLink(TimeStampedModel):
    TYPE_CHOICES = [('note', 'Note'), ('snippet', 'Code Snippet'), ('profile', 'Profile'), ('assignment', 'Assignment')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_links')
    slug = models.SlugField(unique=True, max_length=40, default='', blank=True)
    target_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, blank=True, null=True)
    snippet = models.ForeignKey(CodeSnippet, on_delete=models.CASCADE, blank=True, null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = uuid.uuid4().hex[:18]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.target_type} share for {self.user.username}"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
