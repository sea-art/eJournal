from django.core.exceptions import ValidationError
from VLE.settings.base import USER_MAX_FILE_SIZE_BYTES


# Base 64 image is roughly 37% larger than a plain image
def validate_profile_picture_base64(urlData):
    """Checks if the original size does not exceed 2MB AFTER encoding."""
    if len(urlData) > USER_MAX_FILE_SIZE_BYTES * 1.37:
        raise ValidationError("Max size of file is %s Bytes" % USER_MAX_FILE_SIZE_BYTES)


def validate_user_file(inMemoryUploadedFile):
    """Checks if size does not exceed 2MB."""
    if inMemoryUploadedFile.size > USER_MAX_FILE_SIZE_BYTES:
        raise ValidationError("Max size of file is %s Bytes" % USER_MAX_FILE_SIZE_BYTES)
