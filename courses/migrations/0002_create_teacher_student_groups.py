# Generated by Django 5.1.4 on 2025-01-01 12:42

from django.db import migrations
from django.contrib.auth.models import Group

def create_groups(apps, schema_editor):
    # Create Teacher and Student groups
    teacher_group, created = Group.objects.get_or_create(name='Teacher')
    student_group, created = Group.objects.get_or_create(name='Student')

    if created:
        print("Teacher and Student groups created.")
    else:
        print("Teacher and Student groups already exist.")

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),  # Ensure this depends on the creation of the `Course` model
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]