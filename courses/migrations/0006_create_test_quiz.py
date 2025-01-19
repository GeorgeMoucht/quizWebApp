from django.db import migrations 
from django.utils.timezone import now

def create_test_quiz(apps, schema_editor):
    # Get models dynamically
    Course = apps.get_model('courses', 'Course')
    Quiz = apps.get_model('courses', 'Quiz')
    Question = apps.get_model('courses', 'Question')
    Answer = apps.get_model('courses', 'Answer')

    # Retrieve a test course
    try:
        test_course = Course.objects.get(title='Test Course')
    except Course.DoesNotExist:
        raise Exception("Test Course does not exist. Please create it first.")

    # Create a test quiz
    test_quiz = Quiz.objects.create(
        title="Test Quiz",
        summary="This is a test quiz for the Test Course.",
        score=100.00,  # Total score of the quiz
        published=True,
        published_at=now(),
        course=test_course,
        content="This quiz is designed to test your knowledge of various topics. Answer all questions carefully."
    )

    # Add questions and answers
    questions = [
        {
            "type": 1,  # Multiple Choice
            "level": 1,  # Easy
            "score": 10.00,
            "content": "What is the capital of France?",
            "answers": [
                {"content": "Paris", "is_correct": True},
                {"content": "London", "is_correct": False},
                {"content": "Berlin", "is_correct": False},
            ],
        },
        {
            "type": 2,  # True/False
            "level": 1,  # Easy
            "score": 5.00,
            "content": "The Earth is flat.",
            "answers": [
                {"content": "True", "is_correct": False},
                {"content": "False", "is_correct": True},
            ],
        },
                {
            "type": 1,  # Multiple Choice
            "level": 2,  # Medium
            "score": 15.00,
            "content": "Which of the following is not a programming language?",
            "answers": [
                {"content": "Python", "is_correct": False},
                {"content": "JavaScript", "is_correct": False},
                {"content": "HTML", "is_correct": True},
            ],
        },
        {
            "type": 2,  # True/False
            "level": 2,  # Medium
            "score": 20.00,
            "content": "Water boils at 100 degrees Celsius.",
            "answers": [
                {"content": "True", "is_correct": True},
                {"content": "False", "is_correct": False},
            ],
        },
        {
            "type": 1,  # Multiple Choice
            "level": 3,  # Difficult
            "score": 50.00,
            "content": "Which of the following is a planet in our solar system?",
            "answers": [
                {"content": "Earth", "is_correct": True},
                {"content": "Mars", "is_correct": True},
                {"content": "Sun", "is_correct": False},
            ],
        },
    ]

    # Add questions and answers to the quiz
    for question_data in questions:
        question = Question.objects.create(
            quiz=test_quiz,
            type=question_data["type"],
            active=True,
            level=question_data["level"],
            score=question_data["score"],
            content=question_data["content"]
        )

        for answer_data in question_data["answers"]:
            Answer.objects.create(
                question=question,
                content=answer_data["content"],
                is_correct=answer_data["is_correct"]
            )

    print(f"Test Quiz '{test_quiz.title}' with questions created successfully!")

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_create_test_lesson'),
    ]

    operations = [
        migrations.RunPython(create_test_quiz),
    ]