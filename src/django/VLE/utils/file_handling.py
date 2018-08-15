"""
File handling related utilites.
"""


def get_path(instance, filename):
    """Upload user files into their respective directories. Following MEDIA_ROOT/files/uID/..."""
    return 'files/' + str(instance.author.id) + '/' + filename
