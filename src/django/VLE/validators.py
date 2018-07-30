from django.core.exceptions import ValidationError


# Base 64 image is roughly 37% larger than a plain image
def validate_profile_picture_base64(urlData):
    """Checks if the original size does not exceed 2MB after encoding."""
    limit_mb = 2

    if len(urlData) > limit_mb * 1024 * 1024 * 1.37:
        raise ValidationError("Max size of file is %s MB" % limit_mb)
