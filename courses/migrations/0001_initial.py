import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Create the Course table
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('teacher', models.ForeignKey(limit_choices_to={'groups__name': 'Teacher'},
                                              on_delete=django.db.models.deletion.CASCADE,
                                              related_name='courses',
                                              to=settings.AUTH_USER_MODEL)),
                ('password', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'permissions': [('enroll_in_course', 'Can enroll in course')],
            },
        ),

        # Create the Enrollment table
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolled_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             related_name='enrollments',
                                             to='courses.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='enrollments',
                                              to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('student', 'course')},
            },
        ),

        # Create the Lesson table
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='lessons/attachments')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                             related_name='lessons',
                                             to='courses.Course')),
            ],
        ),

        #Create the Course table
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Τίτλος')),
                ('summary', models.TextField(blank=True, null=True, verbose_name='Σύντομη Περιγραφή')),
                ('type', models.PositiveSmallIntegerField(
                    choices=[
                        (1, 'Multiple Choice'),
                        (2, 'True/False'),
                        (3, 'Short Answer'),
                    ],
                    default=1,
                    verbose_name='Τύπος'
                )),
                ('score', models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name='Βαθμολογία')),
                ('published', models.BooleanField(default=False, verbose_name='Δημοσιευμένο')),
                ('published_at', models.DateTimeField(blank=True, null=True, verbose_name='Ημερομηνία Δημοσίευσης')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Ημερομηνία Δημιουργίας')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ημερομηνία Τελευταίας Ενημέρωσης')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Περιεχόμενο')),
                ('course', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='quizzes',
                    to='courses.Course',
                    verbose_name='Μάθημα'
                )),
            ],
        ),

        # Create the QuizQuestion table
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(
                    choices=[
                    (1, 'Multiple Choice'),
                    (2, 'True/False'),
                    (3, 'Short Answer')
                    ],
                    default=1,
                    verbose_name='Question Type'
                )),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('level', models.PositiveSmallIntegerField(
                    choices=[
                    (1, 'Easy'),
                    (2, 'Medium'),
                    (3, 'Difficult')
                    ],
                    default=1,
                    verbose_name='Difficulty Level'
                )),
                ('score', models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name='Score')),
                ('content', models.TextField(verbose_name='Question Content')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('quiz', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='questions',
                    to='courses.quiz',
                    verbose_name='Quiz'
                )),
            ],
        ),

        # Create the QuizAnswer table
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('correct', models.BooleanField(default=False, verbose_name='Correct')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('content', models.TextField(verbose_name='Content')),
                ('quiz', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='answers',
                    to='courses.Quiz',
                    verbose_name='Quiz'
                )),
                ('question', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='answers',
                    to='courses.Question',
                    verbose_name='Question'
                )),
            ],
        ),

        # Create the Take table
        migrations.CreateModel(
            name='Take',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name='Score')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Started At')),
                ('finished_at', models.DateTimeField(blank=True, null=True, verbose_name='Finished At')),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='takes',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='User'
                )),
                ('quiz', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='takes',
                    to='courses.quiz',
                    verbose_name='Quiz'
                )),
            ],
        ),

        # Create the Take_Answer table
        migrations.CreateModel(
            name='TakeAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('take', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='take_answers',
                    to='courses.take'
                )),
                ('answer', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='take_answers',
                    to='courses.answer'
                )),
            ],
        ),


    ]
   
