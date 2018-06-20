from VLE.models import Node
from VLE.models import Entry


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
            if entry.graded:
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
    return entries.filter(graded=True).count()
# END journal stat functions
