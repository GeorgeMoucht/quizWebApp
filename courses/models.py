from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    """
    Represent a course in the application.

    This model holds information about the course, including the title,
    description, the teacher who created it, and the creation date.
    It is associated with 'User' model through a foreign key, ensuring
    that only users in the 'Teacher' group can be assigned as the
    course teacher.

    Attributes:
        title (str): The title of the course, which should be a short
            and descriptive name.
        description (str): A detailed description of the course content.
        teacher (ForeignKey): The teacher who created the course,
                represented by a 'User'. Only users in the 'Teacher' group
                can be assigned as a teacher.
        created_at (datetime): The timestamp when the course was created.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses',
        limit_choices_to={'groups__name': 'Teacher'}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=100, null=True, blank=True)

    # Define many to many relationship
    students = models.ManyToManyField(
        User,
        through='Enrollment',
        related_name='courses_enrolled',
        blank=True
    )

    class Meta:
        permissions = [
            ('enroll_in_course', 'Can enroll in course')
        ]

    def __str__(self):
        """
        String representation of the course.

        Returns:
            str: A string that returns the course title.
        """
        return self.title

class Lesson(models.Model):
    """
    Represents a lesson in a course.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    attachment = models.FileField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    """
    Represents the enrollment of a student in a course.

    This model tracks which student are enrolled in which courses
    and stores the enrollment date.

    Attributes:
        student (ForeignKey): The student (user) enrolled in the course.
        course (ForeignKey): The course in which the student is enrolled.
        enrolled_at (DateTimeField): The date and time when the student
            enrolled.
    """
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
    
    
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True, null=True)
    type = models.PositiveSmallIntegerField(
        choices=[
            (1, "Multiple Choice"),
            (2, "True/False"),
            (3, "Short Answer")
        ],
        default=1
    )
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True, null=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="quizzes"
    )

    def __str__(self):
        return f"{self.title} ({self.course.title})"


class Question(models.Model):
    """
    Represents a question belonging to a quiz.
    """
    QUESTION_TYPE_CHOICES = [
        (1, "Multiple Choice"),
        (2, "True/False"),
        (3, "Short Answer"),
    ]

    QUESTION_LEVEL_CHOICES = [
        (1, "Easy"),
        (2, "Medium"),
        (3, "Difficult"),
    ]

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Quiz"
    )
    type = models.PositiveSmallIntegerField(
        choices=QUESTION_TYPE_CHOICES,
        default=1,
        verbose_name="Question Type"
    )
    active = models.BooleanField(default=True, verbose_name="Active")
    level = models.PositiveSmallIntegerField(
        choices=QUESTION_LEVEL_CHOICES,
        default=1,
        verbose_name="Difficulty Level"
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name="Score"
    )
    content = models.TextField(verbose_name="Question Content")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"Question: {self.content[:50]} (Quiz: {self.quiz.title})"
    
class Answer(models.Model):
    content = models.TextField()
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    def __str__(self):
        return f"Answer for Question ID {self.question.id}: {self.content[:50]}"

class Take(models.Model):
    """
    Represents an attempt by a user to complete a quiz.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='takes',
        verbose_name="User"
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='takes',
        verbose_name="Quiz"
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name="Score"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Started At"
    )
    finished_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Finished At"
    )

    def __str__(self):
        """
        String representation of the Take.
        """
        return f"User {self.user.username} - Quiz {self.quiz.title} - Score {self.score}"  

class TakeAnswer(models.Model):
    """
    Represents an answer submitted during a quiz attempt.

    Attributes:
        take (ForeignKey): Reference to the Take instance (quiz attempt).
        answer (ForeignKey): Reference to the Answer instance.
        created_at (DateTimeField): Timestamp of when the answer was submitted.
        content (TextField): If the answer is of type 'textarea', stores the content.
    """
    take = models.ForeignKey(
        'Take', 
        on_delete=models.CASCADE, 
        related_name='take_answers'
    )
    answer = models.ForeignKey(
        'Answer', 
        on_delete=models.CASCADE, 
        related_name='take_answers'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"TakeAnswer (Take ID: {self.take.id}, Answer ID: {self.answer.id})"
    
      
    
