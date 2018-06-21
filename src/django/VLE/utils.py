from VLE.models import Node
from VLE.models import Entry
from django.http import JsonResponse


# START: API-POST functions
def get_required_post_params(post, *keys):
    """
    Gets required post parameters, throwing
    KeyError if not peesent.
    """
    result = []
    for key in keys:
        result.append(post[key])
    return result


def get_optional_post_params(post, *keys):
    """
    Gets optional post parameters, filling
    them as None if not present.
    """
    result = []
    for key in keys:
        if key in post:
            result.append(post[key])
        else:
            result.append(None)
    return result


def keyerror_json(*keys):
    if len(keys) == 1:
        return JsonResponse({'result': '400 Bad Request',
                             'description': 'Field {0} is required but is missing.'.format(keys)},
                            status=400)
    else:
        return JsonResponse({'result': '400 Bad Request',
                             'description': 'Fields {0} are required but one or more are missing.'.format(keys)},
                            status=400)
# END: API-POST functions


# START: journal stat functions
def get_journal_entries(journal):
    """Gets the journal entries from a journal.

    - journal: the journal in question.

    Returns a QuerySet of entries from a journal.
    """
    nodes = journal.node_set.all().exclude(type=Node.PROGRESS)
    return Entry.objects.filter(node__in=nodes)


def get_max_points(journal):
    return journal.assignment.format.max_points


def get_acquired_grade(entries, journal):
    """Gets the number of acquired points in an journal.

    - journal: the journal in question.

    Returns the total number of points depending on the grade type.
    """
    format = journal.assignment.format
    entries = get_journal_entries(journal)
    total_grade = 0
    if format.grade_type == 'GR':
        count_graded = 0
        for entry in entries:
            if entry.published:
                count_graded += 1
                total_grade += entry.grade
        return total_gradee
    else:
        for entry in entries:
            total_grade += entry.grade
        return total_grade


def get_submitted_count(entries):
    """Counts the number of submitted entries.

    - entries: the entries to count with.

    Returns the submitted entry count.
    """
    return entries.count()


def get_graded_count(entries):
    """Counts the number of graded entries.

    - entries: the entries to count with.

    Returns the graded entry count.
    """
    return entries.filter(published=True).count()
# END journal stat functions
