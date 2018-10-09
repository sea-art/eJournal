"""
Entry utilities.

A library with utilities related to entries.
"""
from VLE.utils import file_handling


def patch_entry_content(user, entry, old_content, field, data, assignment):
    """Creates new content for an entry, deleting the current content.

    If no temporary file is stored to replace the current content, the old content is kept as is."""
    if field.type in ['i', 'f', 'p']:
        new_file = file_handling.get_temp_user_file(user, assignment, data, content=old_content)

        if new_file:
            # As this get does not rely on user given data, no error should be needed.
            old_file = user.userfile_set.get(author=user, assignment=assignment, node=entry.node, entry=entry,
                                             content=old_content, file_name=old_content.data)
            old_file.delete()
            file_handling.make_permanent_file_content(new_file, old_content, entry.node)

    old_content.data = data
    old_content.save()
