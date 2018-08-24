from django.core.exceptions import ValidationError
import VLE.settings as settings
import re


# Base 64 image is roughly 37% larger than a plain image
def validate_profile_picture_base64(urlData):
    """Checks if the original size does not exceed 2MB AFTER encoding."""
    if len(urlData) > settings.USER_MAX_FILE_SIZE_BYTES * 1.37:
        raise ValidationError("Max size of file is %s Bytes" % settings.USER_MAX_FILE_SIZE_BYTES)


def validate_user_file(inMemoryUploadedFile):
    """Checks if size does not exceed 2MB."""
    if inMemoryUploadedFile.size > settings.USER_MAX_FILE_SIZE_BYTES:
        raise ValidationError("Max size of file is %s Bytes" % settings.USER_MAX_FILE_SIZE_BYTES)


def validate_password(password):
    """Validates password by length, having a capital letter and a special character."""
    if len(password) < 8:
        raise ValidationError("Password needs to contain at least 8 characters.")
    if password == password.lower():
        raise ValidationError("Password needs to contain at least 1 capital letter.")
    if re.match(r'^\w+$', password):
        raise ValidationError("Password needs to contain a special character.")
