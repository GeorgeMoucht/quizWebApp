from django.db import migrations

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

class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0004_enroll_testUser_to_testCourse')
    ]

    operations = [
        migrations.RunPython(create_test_lesson),
    ]