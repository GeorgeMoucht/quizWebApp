from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_create_test_course'),  # Make sure to replace with the correct previous migration
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                (
                    'id', models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'enrolled_at', models.DateTimeField(
                        auto_now_add=True
                    )
                ),
                (
                    'course', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='enrollments',
                        to='courses.course'
                    )
                ),
                (
                    'student', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='enrollments',
                        to='auth.user'
                    )
                )
            ],
            options={
                'unique_together': ('student', 'course'),  # Corrected typo here
            }
        )
    ]
