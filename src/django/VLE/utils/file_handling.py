"""
File handling related utilites.
"""
import shutil
import json
import os
from django.conf import settings


def get_path(instance, filename):
    """Upload user files into their respective directories. Following MEDIA_ROOT/uID/aID/nID/contentID/<file>

    Uploaded files not part of an entry yet, are uploaded to MEDIA_ROOT/uID/-1/<file>, and are treated as temporary
    untill link to an entry."""
    if instance.node is None:
        return str(instance.author.id) + '/-1/' + filename
    else:
        return str(instance.author.id) + '/' + str(instance.assignment.id) + '/' + str(instance.node.id) + '/' \
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


def make_permanent_file_content(user_file, content, node):
    user_file.content = content
    user_file.node = node
    user_file.entry = content.entry
    user_file.save()

    org = os.path.join(settings.MEDIA_ROOT, user_file.file.name)
    dest = str(user_file.author.id) + '/' + str(user_file.assignment.id) + '/' + str(user_file.node.id) + '/' + \
        str(user_file.content.id) + '/' + user_file.file_name
    dest = os.path.join(settings.MEDIA_ROOT, dest)
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    shutil.move(org, dest)
