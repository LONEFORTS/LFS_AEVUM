from django.contrib import admin
from .models import (
    Announcement, Assignment, AttendanceRecord, CodeSnippet, Event,
    FocusSession, Note, Profile, SharedLink, Submission, Tag, Task,
)

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Note)
admin.site.register(Task)
admin.site.register(Event)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(AttendanceRecord)
admin.site.register(Announcement)
admin.site.register(CodeSnippet)
admin.site.register(FocusSession)
admin.site.register(SharedLink)
