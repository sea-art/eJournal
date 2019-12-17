import base64
import os
import pathlib
import re
import uuid
from mimetypes import guess_extension

import django.db.models.deletion
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import migrations, models

import VLE.utils.file_handling


# Expects a string containing a single base64 file
def base64ToContentFile(string, filename):
    matches = re.findall(r'data:(.*);base64,(.*)', string)[0]
    mimetype = matches[0]
    extension = guess_extension(mimetype)
    return ContentFile(base64.b64decode(matches[1]), name='{}{}'.format(filename, extension))


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


# TODO Start expanding
def convertBase64ToFiles(apps, schema_editor):
    Assignment = apps.get_model('VLE', 'Assignment')
    Comment = apps.get_model('VLE', 'Comment')
    Content = apps.get_model('VLE', 'Content')
    Field = apps.get_model('VLE', 'Field')
    User = apps.get_model('VLE', 'User')
    FileContext = apps.get_model('VLE', 'FileContext')

    base64Img = re.compile(r'<img src=\"(data:image\/[^;]+;base64[^\"]+)\" />')

    comments = Comment.objects.all().exclude(author=None)
    for c in comments:
        matches = re.findall(base64Img, c.text)
        for m in matches:
            file_name = 'comment-{}-from-base64-{}'.format(c.pk, uuid.uuid4().hex)
            base64ToContentFile(m, file_name)

            FileContext.objects.create(
                file=base64ToContentFile(m, file_name),
                file_name=file_name,
                author=c.author,
                journal=c.entry.node.journal,
                is_temp=False,
                creation_date=c.creation_date,
                last_edited=c.last_edited,
            )
    # TODO handle comments which have no author but do have base64 images.

    content = Content.objects.filter(field__type='rt')
    for c in content:
        matches = re.findall(base64Img, c.text)

    assignments = Assignment.objects.all()
    for a in assignments:
        matches = re.findall(base64Img, a.description)

    fields = Field.objects.all()
    for f in fields:
        matches = re.findall(base64Img, f.description)

    users = User.objects.all()
    for u in users:
        matches = re.findall(base64Img, u.profile_picture)


class Migration(migrations.Migration):

    dependencies = [
        ('VLE', '0036_mail_username_to_lower_case'),
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
            ],
        ),
        migrations.RunPython(
            # convertUserFiles,
            convertBase64ToFiles,
        ),
    ]
