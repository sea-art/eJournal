# Generated by Django 2.1.7 on 2019-10-04 11:31

import logging

import django.contrib.postgres.fields.citext
from django.contrib.postgres.operations import CITextExtension
from django.db import migrations, models


def mail_username_to_lower(apps, schema_editor):
    logger = logging.getLogger(__name__)
    User = apps.get_model('VLE', 'User')
    for user in User.objects.all():
        u = User.objects.filter(email__iexact=user.email)
        if u.count() == 1 and isinstance(user.email, str):
            user.email = user.email.lower()
            user.save()
        else:
            logger.error('User {} has multiple email matches'.format(user.username))
    for user in User.objects.all():
        u = User.objects.filter(username__iexact=user.username)
        if u.count() == 1 and isinstance(user.username, str):
            user.username = user.username.lower()
            user.save()
        else:
            logger.error('User {} has multiple username matches'.format(user.username))


class Migration(migrations.Migration):

    dependencies = [
        ('VLE', '0035_test_student'),
    ]

    operations = [
        migrations.RunPython(
            mail_username_to_lower,
        ),
        CITextExtension(),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=django.contrib.postgres.fields.citext.CIEmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=django.contrib.postgres.fields.citext.CITextField(max_length=150, unique=True),
        ),
    ]
