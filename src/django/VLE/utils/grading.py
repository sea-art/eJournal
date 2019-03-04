from VLE.models import Comment, Entry


def publish_all_journal_grades(journal, published):
    """publish all grades that are not None for a journal.

    - journal: the journal in question
    - published: either True or False. If True show the grade to student.
    """
    Entry.objects.filter(node__journal=journal).exclude(grade=None).update(published=published)
    if published:
        Comment.objects.filter(entry__node__journal=journal).exclude(entry__grade=None).update(published=True)
