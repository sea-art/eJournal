# Generated by Django 2.1.2 on 2019-02-06 11:26

from django.db import migrations, models

import VLE.utils.file_handling


class Migration(migrations.Migration):

    dependencies = [
        ('VLE', '0014_journal_bonus_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='feedback_file',
            field=models.FileField(null=True, blank=True, upload_to=VLE.utils.file_handling.get_feedback_file_path),
        ),
    ]
