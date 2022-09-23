from django.contrib import admin

from lesson.models import Subject, Group, GroupJournal, AttendanceAndGrades


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']
    list_filter = ['price', ]
    search_fields = ['name', 'price']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'teacher']
    list_filter = ['teacher']
    search_fields = ['name']


@admin.register(GroupJournal)
class GroupJournalAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'group', 'theme']
    list_filter = ['date', 'group']
    search_fields = ['date']


@admin.register(AttendanceAndGrades)
class AttendanceAndGradesAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'group_journal',
        'date',
        'student',
        'status',
        'grade',
    ]
    search_fields = ['id', 'date', 'status']
