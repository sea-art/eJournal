from django.core.exceptions import ValidationError
import magic


# https://www.programcreek.com/python/example/97557/magic.from_buffer
def validate_profile_picture(uploadedFile):
    """To be exanded, currently only checks file size."""
    print('VALIDATING')
    limit_mb = 2

    if uploadedFile.size > limit_mb * 1024 * 1024:
        raise ValidationError("Max size of file is %s MB" % limit_mb)

    # if uploadedFile.multiple_chunks:
    #     raise ValidationError("File size is too large to read from memory, can't validate without writing.")
    # mime = magic.from_buffer(uploadedFile.read(), mime=True)
    # if mime.split('/')[0] != 'image':
    #     raise ValidationError("File mime type to be expected of type image")
    #
    # if uploadedFile.width != uploadedFile.heigth:
    #     raise ValidationError("Profile images should be square!")
