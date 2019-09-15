# Set all latest (highest key) lti ids as the active lti id
# Convert all lti_ids to array fields directly on the Course and Assignment models.

from django.db import migrations


def migrate_lti_ids(apps, schema_editor):
    Course = apps.get_model('VLE', 'Course')
    Assignment = apps.get_model('VLE', 'Assignment')
    Lti_ids = apps.get_model('VLE', 'Lti_ids')

    for course in Course.objects.all():
        lti_ids = Lti_ids.objects.filter(for_model='Course', course=course)
        if lti_ids.exists():
            course.active_lti_id = lti_ids.last().lti_id
            course.save()

    for assignment in Assignment.objects.all():
        lti_ids = Lti_ids.objects.filter(for_model='Assignment', assignment=assignment)
        if lti_ids.exists():
            assignment.active_lti_id = lti_ids.last().lti_id
            assignment.lti_id_set = [lti_id.lti_id for lti_id in lti_ids]
            assignment.save()
            for c in assignment.courses.all():
                for lti_id in lti_ids:
                    if lti_id.lti_id not in c.assignment_lti_id_set:
                        c.assignment_lti_id_set.append(lti_id.lti_id)
                c.save()


# TODO delete Lti_ids table
class Migration(migrations.Migration):

    dependencies = [
        ('VLE', '0027_lti_id_handling'),
    ]

    operations = [
        migrations.RunPython(
            migrate_lti_ids,
        ),
    ]
