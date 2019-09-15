# Set all latest (highest key) lti ids as the active lti id
# Convert all lti_ids to array fields directly on the Course and Assignment models.

import django.contrib.postgres.fields
from django.db import migrations, models


# TODO delete Lti_ids table
class Migration(migrations.Migration):

    dependencies = [
        ('VLE', '0026_preferences_grade_button_setting'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='active_lti_id',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='course',
            name='active_lti_id',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='course',
            name='assignment_lti_id_set',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.TextField(), default=list, size=None),
        ),
        migrations.AddField(
            model_name='assignment',
            name='lti_id_set',
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.TextField(), default=list, size=None),
        ),
    ]
