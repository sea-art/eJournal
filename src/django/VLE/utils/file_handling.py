"""
File handling related utilites.
"""
import json
import os
import re
import shutil

from django.conf import settings

import VLE.models
from VLE.utils.error_handling import VLEBadRequest, VLEPermissionError


def get_path(instance, filename):
    """Upload user files into their respective directories. Following MEDIA_ROOT/uID/aID/<file>

    Uploaded files not part of an entry yet, and are treated as temporary untill linked to an entry."""
    return str(instance.author.id) + '/' + str(instance.assignment.id) + '/' + filename


def get_file_path(file, filename):
    """Upload user files into their respective directories. Following MEDIA_ROOT/uID/<category>/?[id/]<filename>"""
    if file.is_temp:
        return('{}/tempfiles/{}'.format(file.author.id, filename))
    elif file.journal is not None:
        return '{}/journalfiles/{}/{}'.format(file.author.id, file.journal.id, filename)
    elif file.assignment is not None:
        return '{}/assignmentfiles/{}/{}'.format(file.author.id, file.assignment.id, filename)
    elif file.course is not None:
        return '{}/coursefiles/coursefiles/{}/{}'.format(file.author.id, file.course.id, filename)
    else:
        return '{}/userfiles/{}'.format(file.author.id, filename)


def get_feedback_file_path(instance, filename):
    """Upload user feedback file into their respective directory. Following MEDIA_ROOT/uID/feedback/<file>

    An uploaded feedback file is temporary, and removed when the feedback mail is processed by celery."""
    return '{}/feedback/{}'.format(instance.id, filename)


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

    return archive_ouput_path, '{}.{}'.format(archive_name, archive_extension)


def establish_file(author, identifier, course=None, assignment=None, journal=None, content=None, comment=None,
                   in_rich_text=False):
    """establish files, after this they won't be removed."""
    if str(identifier).isdigit():
        file = VLE.models.FileContext.objects.get(pk=identifier)
    else:
        file = VLE.models.FileContext.objects.get(access_id=identifier)

    if file.author != author:
        raise VLEPermissionError('You are not allowed to update files of other users')
    if not file.is_temp:
        raise VLEBadRequest('You are not allowed to update established files')

    if comment:
        journal = comment.entry.node.journal
    if content:
        journal = content.entry.node.journal
    if journal:
        assignment = journal.assignment
    if assignment:
        if not course:
            course = assignment.get_active_course(author)

    file.comment = comment
    file.content = content
    file.journal = journal
    file.assignment = assignment
    file.course = course
    file.is_temp = False
    file.in_rich_text = in_rich_text
    file.save()
    if content and not in_rich_text:
        content.data = str(file.pk)
        content.save()

    return file


def get_files_from_rich_text(rich_text, only_temp=True):
    re_access_ids = re.compile(r'/files/([a-zA-Z0-9]+)/access_id/')
    return [VLE.models.FileContext.objects.get(access_id=access_id)
            for access_id in re.findall(re_access_ids, rich_text)]


def establish_rich_text(author, rich_text, course=None, assignment=None, journal=None, comment=None, content=None):
    if rich_text is None or len(rich_text) < 128:
        return
    for file in get_files_from_rich_text(rich_text):
        if file.is_temp:
            establish_file(author, file.access_id, course, assignment, journal, content, comment, in_rich_text=True)


def remove_unused_user_files(user):
    """Deletes floating user files."""
    # Remove temp images
    VLE.models.FileContext.objects.filter(author=user, is_temp=True).delete()
    # Remove rich_text files
    for file in VLE.models.FileContext.objects.filter(author=user, content__isnull=False):
        if file.content.field.type in VLE.models.Field.FILE_TYPES:  # Check if file is replaced
            if str(file.pk) != file.content.data:
                file.delete()
        elif file.content.field.type == VLE.models.Field.RICH_TEXT:  # Check if file is replaced
            if str(file.access_id) not in file.content.data:
                file.delete()
    for file in VLE.models.FileContext.objects.filter(author=user, comment__isnull=False):
        if str(file.access_id) not in file.comment.text:
            file.delete()
    for file in VLE.models.FileContext.objects.filter(author=user, assignment__isnull=False, journal__isnull=True):
        if str(file.access_id) not in file.assignment.description:
            found = False
            for field in VLE.models.Field.objects.filter(template__format__assignment=file.assignment):
                if str(file.access_id) in field.description:
                    found = True
                    break
            if not found:
                file.delete()
