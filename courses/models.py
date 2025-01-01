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
