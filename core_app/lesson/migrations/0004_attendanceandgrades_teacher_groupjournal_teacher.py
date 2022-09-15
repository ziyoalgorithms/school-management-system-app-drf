# Generated by Django 4.1.1 on 2022-09-14 08:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("lesson", "0003_remove_attendanceandgrades_groupjournal_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendanceandgrades",
            name="teacher",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="attendance_and_grades",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="groupjournal",
            name="teacher",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="group_journals",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
