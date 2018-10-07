"""
Entry utilities.

A library with utilities related to entries.
"""
from VLE.utils import file_handling
import VLE.factory as factory


def replace_entry_content(user, entry, old_content, field, data, assignment):
    """Creates new content for an entry, deleting the current content.

    If no temporary file is stored to replace the current content, the old content is kept as is."""
    if field.type in ['i', 'f', 'p']:
        new_file = file_handling.get_temp_user_file(user, assignment, data, content=old_content)

        if new_file:
            new_content = factory.make_content(entry, data, field)
            file_handling.make_permanent_file_content(new_file, new_content, entry.node)
            print('NEW FILE ' + str(new_file.entry), str(new_file.node), str(new_file.content))
            old_content.delete()
    else:
        old_content.delete()
        factory.make_content(entry, data, field)
