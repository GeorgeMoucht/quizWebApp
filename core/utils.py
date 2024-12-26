def is_teacher(user):
    """
    Check if the given user belongs to the 'Teacher' group.

    Args:
        user (User): The user instance to check.

    Returns:
        bool: True if the user is in the 'Teacher' group, else false.
    """
    return user.groups.filter(name='Teacher').exists()

def is_student(user):
    """
    Check if the given user belongs to the 'Student' group.

    Args:
        user (User): The user instance to check.

    Returns:
        bool: True if the user is in the 'Student' group, else false.
    """
    return user.groups.filter(name='Student').exists()