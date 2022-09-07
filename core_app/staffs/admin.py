from django.contrib import admin

from staffs import models

@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']

@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['fist_name', 'last_name', 'phone']
