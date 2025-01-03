# Generated by Django 5.1.4 on 2025-01-01 16:53

from django.db import migrations
from django.contrib.auth.models import User, Group
from profiles.models import Profile
from django.contrib.auth.hashers import make_password

def create_student_and_teacher_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Group = apps.get_model('auth', 'Group')
    Profile = apps.get_model('profiles', 'Profile')
    
    # Create Student user
    student_user, student_created = User.objects.get_or_create(
        username='testStudent',
        defaults={
            'first_name': 'Alex',
            'last_name': 'Ternti',
            'email': 'student@example.com',
            'is_staff': False,
            'is_superuser': False,
            'password': make_password('password')
        }
    )
    
    # Create Teacher user
    teacher_user, teacher_created = User.objects.get_or_create(
        username='testTeacher',
        defaults={
            'first_name': 'Dimitri',
            'last_name': 'Agusto',
            'email': 'teacher@example.com',
            'is_staff': True,
            'is_superuser': False,
            'password': make_password('password')
        }
    )

    # Assign Student and Teacher groups
    try:
        student_group = Group.objects.get(name='Student')
        teacher_group = Group.objects.get(name='Teacher')

        student_user.groups.add(student_group)
        teacher_user.groups.add(teacher_group)

        # Create Profiles for Student and Teacher users
        Profile.objects.get_or_create(user=student_user, defaults={
            'bio': 'This is a student profile.... blah blah blah...'
        })

        Profile.objects.get_or_create(user=teacher_user, defaults={
            'bio': 'This is teacher profile blah blah blah...'
        })
    except Group.DoesNotExist:
        print("Required groups 'Student' or 'Teacher' do not exist.")


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_create_superuser_with_profile'),
        ('courses', '0002_create_teacher_student_groups')
    ]

    operations = [
        migrations.RunPython(create_student_and_teacher_users)
    ]