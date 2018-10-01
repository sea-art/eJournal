"""
File handling related utilites.
"""
import shutil
import json
import os
from django.conf import settings


def get_path(instance, filename):
    """Upload user files into their respective directories. Following MEDIA_ROOT/uID/aID/node_link/contentID/<file>

    Where node_link can be -1 if the node is not created yet, this file is temporary untill the corresponding entry
    is created."""
    if instance.node is None:
        node_link = '-1'
    else:
        node_link = str(instance.node.id)

    return str(instance.author.id) + '/' + str(instance.assignment.id) + '/' + node_link + '/' \
        + str(instance.content.id) + '/' + filename


def compress_all_user_data(user, extra_data_dict=None, archive_extension='zip'):
    """Compresses all user files found in MEDIA_ROOT/uid into a single archiveself.

    If an extra data dictionary is provided, this is json dumped and included in the archive as
    information.json.
    The archive is stored in MEDIA_ROOT/{username}_data_archive.{archive_extension}.
    Please note that this archive is overwritten if it already exists."""
    user_file_dir_path = os.path.join(settings.MEDIA_ROOT, str(user.id))
    archive_name = user.username + '_data_archive'
    archive_ouput_base_name = os.path.join(settings.MEDIA_ROOT, archive_name)
    archive_ouput_path = archive_ouput_base_name + '.' + archive_extension

    if extra_data_dict:
        extra_data_dump_name = 'information.json'
        extra_data_dump_path = os.path.join(user_file_dir_path, extra_data_dump_name)
        os.makedirs(os.path.dirname(extra_data_dump_path), exist_ok=True)
        with open(extra_data_dump_path, 'w') as file:
            file.write(json.dumps(extra_data_dict))

    shutil.make_archive(archive_ouput_base_name, archive_extension, user_file_dir_path)

    return archive_ouput_path
