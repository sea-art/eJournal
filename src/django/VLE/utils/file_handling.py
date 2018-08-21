"""
File handling related utilites.
"""


def get_path(instance, filename):
    """Upload user files into their respective directories. Following MEDIA_ROOT/files/uID/aID/..."""
    return 'files/' + str(instance.author.id) + '/' + str(instance.assignment.id) + '/' + filename
