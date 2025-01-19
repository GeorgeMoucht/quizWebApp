#from django.db import migrations
from django.db import migrations
import os
from django.core.files import File
from django.conf import settings


def create_test_lesson(apps, schema_editor):
    # Get the models
    Course = apps.get_model('courses', 'Course')
    Lesson = apps.get_model('courses', 'Lesson')

    # Retrieve the course with title "Test Course"
    try:
        test_course = Course.objects.get(title='Test Course')
    except Course.DoesNotExist:
        raise Exception('Test Course does not exist.')
    
    # Create a test lesson
    test_lesson = Lesson.objects.create(
        title='Test Lesson',
        description='This is a test lesson for the Test Course.',
        course=test_course,
    )

    # Define the file path for testLesson.docx (updated path)
    file_path = os.path.join(settings.BASE_DIR, 'staticfiles', 'global', 'lesson_files', 'testLesson.docx')

    # Check if the file exists and add it to the lesson
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            test_lesson.attachment.save('testLesson.docx', File(f),save=False)
            test_lesson.save()
    else:
        raise Exception('testLesson.docx file does not exist.')

class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0004_enroll_testUser_to_testCourse')
    ]

    operations = [
        migrations.RunPython(create_test_lesson),
    ]