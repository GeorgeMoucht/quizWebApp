from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now

class Course(models.Model):
    """
    Represents a course in the application.

    This model holds information about a course, including its title,
    description, the teacher who created it, and the creation date.
    It also manages a many-to-many relationship with students through
    the Enrollment model. The teacher must be a user in the 'Teacher'
    group, and a password can be set for the course (e.g., to restrict
    access).

    Attributes:
        title (str): The title of the course, a shourt and decriptive
            name.
        description (str): A detailed description of the course content.
        teacher (Foreignkey): The teacher who created the course,
            represented by 'User'. Only users in the 'Teacher' group can
            be assigned as teachers.
        created_at (datetime): The timestamp when the course was created.
        password (str): An optional password for the course, stored
            securely.
        student (ManytoManyField): A many-to-many relationship linking
            student (users) who are enrolled in the course.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='courses',
        limit_choices_to={'groups__name': 'Teacher'},
        help_text="Only users in the 'Teacher' group can be assigned as the teacher."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    password = models.CharField(max_length=100, null=True, blank=True)

    # Define many to many relationship with students.
    students = models.ManyToManyField(
        User,
        through='Enrollment',
        related_name='courses_enrolled',
        blank=True
    )

    image = models.ImageField(
        upload_to='courses/',
        null=True,
        blank=True,
        help_text="Optional images for the course."
    )

    class Meta:
        # Permissions for users to enroll in courses
        permissions = [
            ('enroll_in_course', 'Can enroll in course')
        ]

    def __str__(self):
        """
        String representation of the course.

        Returns:
            str: The course title.
        """
        return self.title
    
    def clean(self): 
        """
        Custom validation to ensure the teacher is in the 'Teacher'
        group.

        Raises:
            ValidationError: If the teacher is not part of the 
            'Teacher' group.
        """
        if not self.teacher.groups.filter(name="Teacher").exists():
            raise ValidationError(f"The user {self.teacher} is not in the 'Teacher' group.")

    def save(self, *args, **kwargs):
        """
        Override the save method to has the password if provided,
        and ensure the course passes validation before saving

        Args:
            *args: Positional argument passed to the superclass's 
                save method.
            **kwargs: Keyword arguments passed to the superclass's
                save method.
        """
        # Hash the password if provided
        if self.password:
            self.password = make_password(self.password)
        # Run custom validation
        self.clean()
        # Call the superclass's save method to add course in db.
        super().save(*args, **kwargs)


class Lesson(models.Model):
    """
    Represents a leson in a course.

    This model tracks individual lessons, their titles, descriptions,
    attachements, and the course they belong to. It also tracks when
    the lesson was created and last updated.
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
        student (ForeignKey): The student (user) enrolled in the 
            course.
        course (ForeignKey): The course in which the student 
            is enrolled.
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
        # unique_together = ('student', 'course')
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_enrollment'       
            )
        ]

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
    
    
class Quiz(models.Model):
    """
    Represents a quiz associated with a course.

    Attributes:
        title (str): The title of the quiz.
        summary (str): A short description of the quiz.
        type (int): The type of quiz (Multiple Choice, True/False,
            Short Answer).
        score (float): The maximum score for the quiz.
        published (bool): Whether the quiz is published or not.
        published_at (datetime): The data and time when the quiz was
            published.
        created_at (datetime): The date and time when the quiz was
            created.
        updated_at (datetime): The date and time when the quiz was
            last updated.
        content (str): Additional content/instructions for the quiz.
        course: (ForeignKey): The course associated with the quiz.
    """
    title = models.CharField(max_length=255, verbose_name="Quiz Title")
    summary = models.TextField(
        blank=True,
        null=True,
        verbose_name="Quiz Summary"
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name="Maximum Score"
    )
    published = models.BooleanField(
        default=False,
        verbose_name="Published"
    )
    published_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Published At"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Last Updated"
    )
    content = models.TextField(
        blank=True,
        null=True,
        verbose_name="Additional Content"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="quizzes",
        verbose_name="Course"
    )

    def __str__(self):
        return f"{self.title} ({self.course.title})"
    
    def save(self, *args, **kwargs):
        # Auto-set `published` is True and `published_at`
        # is not already set.
        if self.published and not self.published_at:
            self.published_at = now()
        super().save(*args, **kwargs)


class Question(models.Model):
    """
    Represents a question belonging to a quiz.

    Attributes:
        quiz (ForeignKey): The quiz the question belongs to.
        type (int): The type of question (Multiple Choice, True/False,
            Short Answer).
        active (bool): Whether the question is active.
        level (int): The difficulty level of the question.
        score (float): The score for the question.
        content (str): The actual question text.
        created_at (datetime): When the question was created.
        updated_at (datetime): When the question was last updated.
    """
    MULTIPLE_CHOICE = 1
    TRUE_FALSE = 2
    SHORT_ANSWER = 3

    QUESTION_TYPE_CHOICES = [
        (MULTIPLE_CHOICE, "Multiple Choice"),
        (TRUE_FALSE, "True/False"),
        (SHORT_ANSWER, "Short Answer"),
    ]

    # Question Level Choices
    EASY = 1
    MEDIUM = 2
    DIFFICULT = 3

    QUESTION_LEVEL_CHOICES = [
        (EASY, "Easy"),
        (MEDIUM, "Medium"),
        (DIFFICULT, "Difficult")
    ]

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Quiz"
    )
    type = models.PositiveSmallIntegerField(
        choices=QUESTION_TYPE_CHOICES,
        default=MULTIPLE_CHOICE,
        verbose_name="Question Type"
    )
    active = models.BooleanField(default=True, verbose_name="Active")
    level = models.PositiveSmallIntegerField(
        choices=QUESTION_LEVEL_CHOICES,
        default=EASY,
        verbose_name="Difficulty Level"
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name="Score"
    )
    content = models.TextField(verbose_name="Question Content")
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Created At"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At"
    )

    def __str__(self):
        return f"Question: {self.content[:50]} (Quiz: {self.quiz.title})"
    
class Answer(models.Model):
    """
    Represents an answer belonging to a question.

    Attributes:
        question (ForeignKey): The question this answer belongs to.
        content (str): The answer text.
        is_correct (bool): Whether this answer is the correct one.
        created_at (datetime): When the answer was created.
        updated_at (datetime): When the answer was last updated.
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Question"
    )
    content = models.TextField(verbose_name="Answer Content")
    is_correct = models.BooleanField(
        default=False,
        verbose_name="Is Correct"    
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"    
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At"    
    )

    def clean(self):
        """
        Custom validation to ensure the correct number of valid answers based on the question type.
        """
        question_type = self.question.type

        if question_type == self.question.TRUE_FALSE:
            if self.is_correct and self.question.answers.filter(is_correct=True).exclude(id=self.id).exists():
                raise ValidationError("A True/False question can only have one correct answer.")



    def __str__(self):
        return f"Answer for Question ID {self.question.id}: {self.content[:50]}"

class Take(models.Model):
    """
    Represents an attempt by user to complete a quiz.

    Attributes:
        user (ForeignKey): the user attempting the quiz.
        quiz (Foreignkey): The quiz being attempted.
        score (float): The score achieved by the user.
        created_at (datetime): The timestamp when the attempt started.
        finished_at (datetime): The timestamp when the attempt was
            completed.
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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'quiz'],
                name='unique_user_quiz_take'
            )
        ]
    
    def clean(self):
        """
        Custom validation to ensure `finished_at` is later than
        the `created_at` datetime.
        """
        if self.finished_at and self.finished_at <= self.created_at:
            raise ValidationError("Finished time must be later than the started time.")
        
    def duration(self):
        """
        Calculate the duration of the quiz attempt if finished.

        Returns:
            timedelta or None: The duration of the quiz attempt, or 
                None if the quiz never finished.
        """
        if self.finished_at:
            return self.finished_at - self.created_at
        return None

    def __str__(self):
        """
        String representation of the Take.
        """
        status = "Complete" if self.finished_at else "In Progress"
        return f"User {self.user.username} - Quiz {self.quiz.title} - Score {self.score} - Status: {status}"



class TakeAnswer(models.Model):
    """
    Represents an answer submitted during a quiz attempt.

    Attributes:
        take (ForeignKey): Reference to the Take instance 
            (quiz attempt).
        answer (ForeignKey): Reference to the Answer instance.
        created_at (DateTimeField): Timestamp of when the answer was
            submitted.
        content (TextField): If the answer is of type 'textarea',
            stores the content.
    """
    take = models.ForeignKey(
        'Take', 
        on_delete=models.CASCADE, 
        related_name='take_answers',
        verbose_name="Quiz Attempt"
    )
    answer = models.ForeignKey(
        'Answer',
        on_delete=models.CASCADE,
        related_name='take_answers',
        verbose_name="Answer"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Submitted At"
    )
    content = models.TextField(
        blank=True,
        null=True,
        verbose_name="Answer Content"
    )


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['take', 'answer'],
                name='unique_take_answer'
            ),
            # Ensure no duplicate entries for short-answer questions
            models.UniqueConstraint(
                fields=['take', 'content'],
                name='unique_take_content'
            ),
        ]
    

    def clean(self):
        """
        Custom validation to ensure content is provided for
        open-ended questions.
        """
        if self.answer and self.answer.question.type == Question.SHORT_ANSWER and not self.content:
            raise ValidationError("Content is required for short answer questions.")

    def __str__(self):
        """
        String representation of the TakeAnswer.
        """
        return f"TakeAnswer (Take ID: {self.take.id}, Answer: {self.answer or self.content})"

    
      
    
