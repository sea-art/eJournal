"""
Entry utilities.

A library with utilities related to entries.
"""
import VLE.utils.generic_utils as utils
from VLE.utils import file_handling
from VLE.models import Field, Content
import VLE.factory as factory
from django.core.exceptions import ValidationError


def get_validated_field_and_content(content, entry):
    """Returns the current Content object, as well as the corresponding field and new data to be placed in the old
    content object."""
    try:
        content_id, field_id, data = utils.required_params(content, 'contentID', 'id', 'data')
    except KeyError as e:
        raise e

    try:
        old_content = entry.content_set.get(pk=content_id)
        field = Field.objects.get(pk=field_id)
    except (Field.DoesNotExist, Content.DoesNotExist):
        raise ValidationError('Field or content does not exist.')

    if old_content.field.pk != field.pk:
        raise ValidationError('The given content does not match the accompanying field type.')

    return old_content, field, data


def patch_entry_content(user, entry, old_content, field, data, assignment):
    """Creates new content for an entry, deleting the current contentself.

    If no temporary file is stored to replace the current content, the old content is kept as is."""
    if field.type in ['i', 'f', 'p']:
        new_file = file_handling.get_temp_user_file(user, assignment, data, entry=entry, node=entry.node,
                                                    content=old_content)
        if new_file:
            new_content = factory.make_content(entry, data, field)
            file_handling.make_permanent_file_content(new_file, new_content, entry.node)
            old_content.delete()
    else:
        old_content.delete()
        factory.make_content(entry, data, field)
