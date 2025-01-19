from django.db import migrations
from django.utils.timezone import now

def populate_take_and_takeanswer(apps, schema_editor):
    # Get models dynamically
    User = apps.get_model('auth', 'User')
    Quiz = apps.get_model('courses', 'Quiz')
    Take = apps.get_model('courses', 'Take')
    TakeAnswer = apps.get_model('courses', 'TakeAnswer')
    Answer = apps.get_model('courses', 'Answer')

    # Retrieve the test user
    try:
        test_user = User.objects.get(username='testStudent')
    except User.DoesNotExist:
        raise Exception("User 'testStudent' does not exist. Please create it first.")

    # Retrieve the test quiz
    try:
        test_quiz = Quiz.objects.get(title='Test Quiz')
    except Quiz.DoesNotExist:
        raise Exception("Quiz 'Test Quiz' does not exist. Please create it first.")

    # Create a Take for the test user
    take = Take.objects.create(
        user=test_user,
        quiz=test_quiz,
        score=90.00,  # Example score
        created_at=now(),
        finished_at=now()
    )

    # Retrieve all answers for the test quiz
    for question in test_quiz.questions.all():
        correct_answers = question.answers.filter(is_correct=True)

        for answer in correct_answers:
            TakeAnswer.objects.create(
                take=take,
                answer=answer,
                created_at=now(),
                content=answer.content if question.type == 3 else None
            )

    print(f"Take for quiz '{test_quiz.title}' and associated answers created successfully!")

class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0006_create_test_quiz'),
    ]

    operations = [
        migrations.RunPython(populate_take_and_takeanswer),
    ]