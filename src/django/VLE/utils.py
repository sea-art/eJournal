"""
Utilities.

A library with useful functions.
"""
from VLE.models import Entry
from django.http import JsonResponse


# START: API-POST functions
def get_required_post_params(post, *keys):
    """Get required post parameters, throwing KeyError if not present."""
    result = []
    for key in keys:
        result.append(post[key])
    return result


def get_optional_post_params(post, *keys):
    """Get optional post parameters, filling them as None if not present."""
    result = []
    for key in keys:
        if key in post:
            if post[key] == '':
                result.append(None)
            else:
                result.append(post[key])
        else:
            result.append(None)
    return result


def keyerror_json(*keys):
    """Generate a JsonResponse when the JSON has keyerror(s)."""
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
    """Get the journal entries from a journal.

    - journal: the journal in question.

    Returns a QuerySet of entries from a journal.
    """
    return Entry.objects.filter(node__journal=journal)


def get_max_points(journal):
    """Get the maximum amount of points for an assignment."""
    return journal.assignment.format.max_points


def get_acquired_grade(entries, journal):
    """Get the number of acquired points in an journal.

    - journal: the journal in question.

    Returns the total number of points depending on the grade type.
    """
    format = journal.assignment.format
    total_grade = 0
    if format.grade_type == 'GR':
        count_graded = 0
        for entry in entries:
            if entry.published:
                count_graded += 1
                total_grade += entry.grade if entry.grade is not None else 0
        return total_grade
    else:
        for entry in entries:
            total_grade += entry.grade if entry.grade is not None else 0
        return total_grade


def get_submitted_count(entries):
    """Count the number of submitted entries.

    - entries: the entries to count with.

    Returns the submitted entry count.
    """
    return entries.count()


def get_graded_count(entries):
    """Count the number of graded entries.

    - entries: the entries to count with.

    Returns the graded entry count.
    """
    return entries.filter(published=True).count()
# END journal stat functions


# START grading functions
def publish_all_assignment_grades(assignment, published):
    """Set published all not None grades from an assignment.

    - assignment: the assignment in question
    - published: either True or False. If True show the grade to student.
    """
    Entry.objects.filter(node__journal__assignment=assignment).exclude(grade=None).update(published=published)


def publish_all_journal_grades(journal, published):
    """Set published all not None grades from a journal.

    - journal: the journal in question
    - published: either True or False. If True show the grade to student.
    """
    Entry.objects.filter(node__journal=journal).exclude(grade=None).update(published=published)
# END grading functions
