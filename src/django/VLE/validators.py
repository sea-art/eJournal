from django.core.exceptions import ValidationError


# https://www.programcreek.com/python/example/97557/magic.from_buffer
def validate_profile_picture(uploadedFile):
    """Checks if the blob size does not exceed 2MB."""
    limit_mb = 2

    if uploadedFile.size > limit_mb * 1024 * 1024:
        raise ValidationError("Max size of file is %s MB" % limit_mb)
