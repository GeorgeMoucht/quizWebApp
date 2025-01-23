# Generated by Django 5.1.4 on 2025-01-03 18:13

from django.db import migrations
from django.core.files import File
import os

def create_test_courses(apps, schema_editor):
    # Get the models dynamically
    User = apps.get_model('auth', 'User')
    Course = apps.get_model('courses', 'Course')

    # Find the test teacher user
    test_teacher = User.objects.filter(username='testTeacher').first()

    if not test_teacher:
        return

    # 1. Create "Test Course"
    test_course = Course.objects.create(
        title='Test Course',
        description='This is a test course for testing purposes.',
        teacher=test_teacher,
        password='coursepassword'
    )

    test_image_path = os.path.join(
        os.path.dirname(__file__),
        '../../media/courses/test_image.jpg'
    )

    if os.path.exists(test_image_path):
        with open(test_image_path, 'rb') as img_file:
            test_course.image.save(
                'test_image.jpg',
                File(img_file), 
                save=True
            )

    # 2. Create "Mathematics" Course
    math_course = Course.objects.create(
        title='Mathematics',
        description=(
            'Dive into the world of algebra, geometry, and basic arithmetic. '
            'Designed to strengthen fundamental math skills and logical thinking.'
        ),
        teacher=test_teacher,
        password='math123'
    )

    # Attach image to "Mathematics" course
    math_image_path = os.path.join(
        os.path.dirname(__file__),
        '../../media/courses/math_image.jpg'
    )

    if os.path.exists(math_image_path):
        with open(math_image_path, 'rb') as math_img_file:
            math_course.image.save(
                'math_image.jpg',
                File(math_img_file),
                save=True
            )

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_create_teacher_student_groups'),
    ]

    operations = [
        migrations.RunPython(create_test_courses)
    ]
