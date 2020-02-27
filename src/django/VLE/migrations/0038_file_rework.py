import base64
import logging
import re
import uuid
from mimetypes import guess_extension

import django.db.models.deletion
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import migrations, models

import VLE.utils.file_handling

logger = logging.getLogger(__name__)
base64ImgEmbedded = re.compile(r'<img\s+src=\"(data:image\/[^;]+;base64[^\"]+)\"\s*/>')


# Expects a string containing a single base64 file
def base64ToContentFile(string, filename):
    matches = re.findall(r'data:(.*);base64,(.*)', string)[0]
    mimetype = matches[0]
    extension = guess_extension(mimetype)
    return ContentFile(base64.b64decode(matches[1]), name='{}{}'.format(filename, extension))


def fileToEmbdeddedImageLink(file):
    return '<img src="{}"/>'.format(file.dowload_url())


def convertUserFiles(apps, schema_editor):
    UserFile = apps.get_model('VLE', 'UserFile')
    FileContext = apps.get_model('VLE', 'FileContext')

    # Delete temp files
    UserFile.objects.filter(content=None).delete()

    for f in UserFile.objects.all():
        # Works once per file retrieval
        FileContext.objects.create(
            file=ContentFile(f.file.file.read(), name=f.file_name),
            file_name=f.file_name,
            author=f.author,
            journal=f.content.entry.node.journal,
            is_temp=False,
            creation_date=f.creation_date,
            last_edited=f.last_edited,
            content=f.content,
        )
        f.delete()

    remaining_user_files = UserFile.objects.all()
    if remaining_user_files.exists():
        logger.error('UserFiles {} still exist.'.format([f.pk for f in remaining_user_files]))


def convertBase64CommentsToFiles(apps, schema_editor):
    Comment = apps.get_model('VLE', 'Comment')
    FileContext = apps.get_model('VLE', 'FileContext')

    for c in Comment.objects.all():
        if c.author is None and re.search(base64ImgEmbedded, c.text):
            logger.error('Comment {} contains base64 images without author'.format(c.id))
            continue

        def createEmbbededCommentFiles(str_match):
            file_name = 'comment-{}-from-base64-{}'.format(c.pk, uuid.uuid4().hex)

            f = FileContext.objects.create(
                file=base64ToContentFile(str_match, file_name),
                file_name=file_name,
                author=c.author,
                journal=c.entry.node.journal,
                is_temp=False,
                creation_date=c.creation_date,
                last_edited=c.last_edited,
            )

            return fileToEmbdeddedImageLink(f)

        c.text = re.sub(base64ImgEmbedded, createEmbbededCommentFiles, c.text)
        c.save()


def convertBase64ContentsToFiles(apps, schema_editor):
    Content = apps.get_model('VLE', 'Content')
    FileContext = apps.get_model('VLE', 'FileContext')

    for c in Content.objects.filter(field__type='rt'):
        def createEmbbededContentFiles(str_match):
            file_name = 'content-{}-from-base64-{}'.format(c.pk, uuid.uuid4().hex)

            f = FileContext.objects.create(
                file=base64ToContentFile(str_match, file_name),
                file_name=file_name,
                author=c.entry.node.journal.user,
                journal=c.entry.node.journal,
                is_temp=False,
                creation_date=c.entry.creation_date,
                last_edited=c.entry.last_edited,
            )

            return fileToEmbdeddedImageLink(f)

        c.data = re.sub(base64ImgEmbedded, createEmbbededContentFiles, c.data)
        c.save()


def convertBase64AssignmentDescriptionsToFiles(apps, schema_editor):
    Assignment = apps.get_model('VLE', 'Assignment')
    FileContext = apps.get_model('VLE', 'FileContext')

    for a in Assignment.objects.all():
        if a.author is None and re.search(base64ImgEmbedded, a.description):
            logger.error('Assignment {} description contains base64 images without author'.format(a.id))
            continue

        def createEmbbededAssignmentDescriptionFiles(str_match):
            file_name = 'assignment-description-{}-from-base64-{}'.format(a.pk, uuid.uuid4().hex)

            f = FileContext.objects.create(
                file=base64ToContentFile(str_match, file_name),
                file_name=file_name,
                author=a.author,
                assignment=a,
                is_temp=False,
                creation_date=a.creation_date,
                last_edited=a.last_edited,
            )

            return fileToEmbdeddedImageLink(f)

        a.description = re.sub(base64ImgEmbedded, createEmbbededAssignmentDescriptionFiles, a.description)
        a.save()


def convertBase64FieldDescriptionsToFiles(apps, schema_editor):
    Field = apps.get_model('VLE', 'Field')
    FileContext = apps.get_model('VLE', 'FileContext')
    Assignment = apps.get_model('VLE', 'Assignment')

    for field in Field.objects.all():
        assignment = Assignment.objects.get(format=field.template.format)
        if assignment.author is None and re.search(base64ImgEmbedded, field.description):
            logger.error('Field {} description contains base64 images without author'.format(field.id))
            continue

        def createEmbbededFieldDescriptionFiles(str_match):
            file_name = 'field-description-{}-from-base64-{}'.format(field.pk, uuid.uuid4().hex)

            f = FileContext.objects.create(
                file=base64ToContentFile(str_match, file_name),
                file_name=file_name,
                author=assignment.author,
                assignment=assignment,
                is_temp=False,
                # QUESTION: Should we add these dates to a template?
                creation_date=assignment.creation_date,
                last_edited=assignment.last_edited,
            )

            return fileToEmbdeddedImageLink(f)

        field.description = re.sub(base64ImgEmbedded, createEmbbededFieldDescriptionFiles, field.description)
        field.save()


def convertBase64ProfilePicturesToFiles(apps, schema_editor):
    User = apps.get_model('VLE', 'User')
    FileContext = apps.get_model('VLE', 'FileContext')
    base64Img = re.compile(r'data:image\/[^;]+;base64[^\"]+')

    for u in User.objects.all():
        match = re.search(base64Img, u.profile_picture)
        if match:
            file_name = 'profile-picture-from-base64-{}'.format(uuid.uuid4().hex)

            f = FileContext.objects.create(
                file=base64ToContentFile(match.group(0), file_name),
                file_name=file_name,
                author=u,
                is_temp=False,
            )

            u.profile_picture = f.download_url()
            u.save()


class Migration(migrations.Migration):

    dependencies = [
        ('VLE', '0037_assignment_assigned_groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileContext',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=VLE.utils.file_handling.get_file_path)),
                ('file_name', models.TextField()),
                ('is_temp', models.BooleanField(default=True)),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_edited', models.DateTimeField()),
                ('assignment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='VLE.Assignment')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('content', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='VLE.Content')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='VLE.Course')),
                ('journal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='VLE.Journal')),
                ('access_id', models.CharField(default=VLE.models.access_gen, max_length=64)),
            ],
        ),
        migrations.RunPython(convertUserFiles),
        migrations.RunPython(convertBase64CommentsToFiles),
        migrations.RunPython(convertBase64ContentsToFiles),
        migrations.RunPython(convertBase64AssignmentDescriptionsToFiles),
        migrations.RunPython(convertBase64FieldDescriptionsToFiles),
        migrations.RunPython(convertBase64ProfilePicturesToFiles),
    ]
