from django.db import migrations, models


def sensible_lti_names(apps, schema_editor):
    Group = apps.get_model('VLE', 'Group')
    Course = apps.get_model('VLE', 'Course')
    for course in Course.objects.all():
        groups = Group.objects.filter(course=course, lti_id=models.F('name'))
        for group in groups:
            n_groups = Group.objects.filter(course=course, pk__lt=group.pk).count()
            group.name = 'Group {:d}'.format(n_groups + 1)
            group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('VLE', '0032_preset_node_fix'),
    ]

    operations = [
        migrations.RunPython(
            sensible_lti_names,
        ),
    ]
