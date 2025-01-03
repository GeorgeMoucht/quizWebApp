# Generated by Django 5.1.4 on 2025-01-03 18:13

from django.db import migrations


def create_test_course(apps, schema_editor):
    # Get the models dynamically
    User = apps.get_model('auth', 'User')
    Course = apps.get_model('courses', 'Course')

    # Find the test teacher user
    test_teacher = User.objects.filter(username='testTeacher').first()

    if test_teacher:
        # Create a test course if the teacher exists
        Course.objects.create(
            title='Test Course',
            description='This is a test course for testing purposes.',
            teacher=test_teacher
        )

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_create_teacher_student_groups'),
    ]

    operations = [
        migrations.RunPython(create_test_course)
    ]
