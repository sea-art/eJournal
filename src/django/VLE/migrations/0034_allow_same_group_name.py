# Generated by Django 2.2.6 on 2019-10-17 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('VLE', '0033_sensible_lti_group_names'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='group',
            unique_together={('lti_id', 'course')},
        ),
    ]
