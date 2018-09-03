from django.core.exceptions import ValidationError
from VLE.settings.production import USER_MAX_FILE_SIZE_BYTES
from django.core.validators import URLValidator
from VLE.models import Field
import re


# Base 64 image is roughly 37% larger than a plain image
def validate_profile_picture_base64(urlData):
    """Checks if the original size does not exceed 2MB AFTER encoding."""
    if len(urlData) > USER_MAX_FILE_SIZE_BYTES * 1.37:
        raise ValidationError("Max size of file is %s Bytes" % USER_MAX_FILE_SIZE_BYTES)


def validate_user_file(inMemoryUploadedFile):
    """Checks if size does not exceed 2MB."""
    if inMemoryUploadedFile.size > USER_MAX_FILE_SIZE_BYTES:
        raise ValidationError("Max size of file is %s Bytes" % USER_MAX_FILE_SIZE_BYTES)


def validate_password(password):
    """Validates password by length, having a capital letter and a special character."""
    if len(password) < 8:
        raise ValidationError("Password needs to contain at least 8 characters.")
    if password == password.lower():
        raise ValidationError("Password needs to contain at least 1 capital letter.")
    if re.match(r'^\w+$', password):
        raise ValidationError("Password needs to contain a special character.")


TEXT = 't'
RICH_TEXT = 'rt'
IMG = 'i'
FILE = 'f'
VIDEO = 'v'
PDF = 'p'
URL = 'u'


def validate_entry_content(content_list):
    """Validates the given data based on its field type, any validation error will be raised."""
    for content in content_list:
        data = content['data']
        tag = content['tag']
        field = Field.objects.get(pk=tag)

        if field.type is URL:
            try:
                url_validate = URLValidator(schemes=('http', 'https', 'ftp', 'ftps'))
                url_validate(data)
            except ValidationError as e:
                raise e
