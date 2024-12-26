from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User, Group, Permission
from django.dispatch import receiver

@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
    """
    Signal handler to assign a default group to newly created users.
    This will assign the 'Student' group to any new user.
    """
    if created:
        # Get or create the 'Student' group
        student_group, _ = Group.objects.get_or_create(name='Student')
        # Add the new user to the 'Student' group
        instance.groups.add(student_group)

        # Check if the user is a teacher and assign teacher permissions
        if instance.groups.filter(name="Teacher").exists():
            assign_teacher_permissions(instance)

@receiver(m2m_changed, sender=User.groups.through)
def assign_teacher_permissions_on_group_change(sender, instance, action, **kwargs):
    """
    This signal is triggered when a user's groups are changed.
    If the user is added to the 'Teacher' group, assign the necessary permissions.
    """
    if action == "pre_add":
        if 'Teacher' in Group.objects.filter(id__in=kwargs['pk_set']).values_list('name', flat=True):
            assign_teacher_permissions(instance)


def assign_teacher_permissions(instance):
    """
    Assign teacher-specific permissions to the Teacher group.
    This function is called when the application starts or when permissions need to be set.
    """
    # Get or create the Teacher group
    teacher_group, created = Group.objects.get_or_create(name="Teacher")

    # Define the permissions we want to assign
    permissions = [
        "add_course",   # Can add a course
        "change_course", # Can change a course
        "delete_course", # Can delete a course
        "view_course",   # Can view a course (Optional)
    ]

    # Add permissions to the Teacher group
    for perm_codename in permissions:
        permission, perm_created = Permission.objects.get_or_create(codename=perm_codename)
        teacher_group.permissions.add(permission)
        if perm_created:
            print(f"Permission '{perm_codename}' created and assigned to Teacher group.")

    print("Permissions successfully assigned to the Teacher group.")
