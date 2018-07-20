from django.core.exceptions import ValidationError


def validate_profile_picture(file):
    """To be exanded, currently only checks file size."""
    print('VALIDATING')
    limit_mb = 2
    if file.size > limit_mb:
        raise ValidationError("Max size of file is %s MB" % limit_mb)
