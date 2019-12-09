import base64
import re
from mimetypes import guess_extension

from django.db import migrations, models


def base64ToFile(string):
    matches = re.findall(r'data:(.*);base64,(.*)', string)[0]
    mimetype = matches[0]
    extension = guess_extension(mimetype)
    filename = '/path/name' + extension  # TODO
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(matches[1]))

def convertBase64ToFiles(apps, schema_editor):
    Assignment = apps.get_model('VLE', 'Assignment')
    Comment = apps.get_model('VLE', 'Comment')
    Content = apps.get_model('VLE', 'Content')
    Field = apps.get_model('VLE', 'Field')

    base64Img = re.compile(r'<img src=\"(data:image\/[^;]+;base64[^\"]+)\" />')

    comments = Comment.objects.all()
    for c in comments:
        matches = re.findall(base64Img, c.text)[0]

    content = Content.objects.filter(field__type=Field.RICH_TEXT)
    for c in content:
        matches = re.findall(base64Img, c.text)[0]

    assignments = Assignment.objects.all()
    for a in assignments:
        matches = re.findall(base64Img, a.description)[0]

    fields = Field.objects.all()
    for f in fields:
        matches = re.findall(base64Img, f.description)[0]


class Migration(migrations.Migration):

    dependencies = [
        ('VLE', '0035_test_student'),
    ]

    operations = [
        migrations.RunPython(
            convertBase64ToFiles,
        ),
    ]
