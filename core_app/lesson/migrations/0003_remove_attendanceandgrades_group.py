# Generated by Django 4.1.1 on 2022-09-18 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("lesson", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="attendanceandgrades", name="group",),
    ]
