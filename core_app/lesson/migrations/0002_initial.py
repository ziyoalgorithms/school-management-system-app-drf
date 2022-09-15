# Generated by Django 4.1.1 on 2022-09-10 21:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("staffs", "0001_initial"),
        ("lesson", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="group",
            name="students",
            field=models.ManyToManyField(related_name="group", to="staffs.student"),
        ),
        migrations.AddField(
            model_name="group",
            name="teacher",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="my_groups",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="attendanceandgrades",
            name="groupjournal",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attendance_and_grade",
                to="lesson.groupjournal",
            ),
        ),
        migrations.AddField(
            model_name="attendanceandgrades",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attendance_and_grades",
                to="staffs.student",
            ),
        ),
    ]