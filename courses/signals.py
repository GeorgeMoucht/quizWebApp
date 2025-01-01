from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Course

@receiver(post_migrate)
def assign_teacher_student_permissions(sender, **kwargs):
    # Get the ContentType for the Course model
    content_type = ContentType.objects.get_for_model(Course)

   # Get the Teacher and Student groups
    teacher_group, _ = Group.objects.get_or_create(name='Teacher')
    student_group, _ = Group.objects.get_or_create(name='Student')

    # Define permissions for Teacher and Student group
    teacher_permissions = ['add_course', 'change_course', 'delete_course']
    student_permissions = ['view_course', 'enroll_in_course']
    
    # Assign permissions to Teacher group
    for perm_codename in teacher_permissions:
        permission, created = Permission.objects.get_or_create(codename=perm_codename, content_type=content_type)
        if created:  # If the permission is newly created
            # Fill in the name if it's missing
            if not permission.name:
                permission.name = f"Can {perm_codename.replace('_', ' ')} course"
                permission.save()
            teacher_group.permissions.add(permission)
            # Uncomment the next line for debugging
            # print(f"Permission '{perm_codename}' added to Teacher group.")

    # Assign permissions to Student group
    for perm_codename in student_permissions:
        permission, created = Permission.objects.get_or_create(codename=perm_codename, content_type=content_type)
        if created:  # If the permission is newly created
            # Fill in the name if it's missing
            if not permission.name:
                permission.name = f"Can {perm_codename.replace('_', ' ')} course"
                permission.save()
            student_group.permissions.add(permission)
            # Uncomment the next line for debugging
            # print(f"Permission '{perm_codename}' added to Student group.")