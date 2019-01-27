# Generated by Django 2.1.2 on 2019-01-27 14:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VLE', '0013_user_preferences'),
    ]

    operations = [
        migrations.RenameField(
            model_name='preferences',
            old_name='show_format_editor_tutorial',
            new_name='show_format_tutorial',
        ),
        migrations.RemoveField(
            model_name='user',
            name='comment_notifications',
        ),
        migrations.RemoveField(
            model_name='user',
            name='grade_notifications',
        ),
        migrations.AddField(
            model_name='preferences',
            name='comment_notifications',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='preferences',
            name='grade_notifications',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='preferences',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
