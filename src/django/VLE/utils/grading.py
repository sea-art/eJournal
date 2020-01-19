
from django.conf import settings
from VLE import factory
from VLE.models import Comment, Entry
from VLE.lti_grade_passback import GradePassBackRequest


def publish_all_journal_grades(journal, author):
    """publish all grades that are not None for a journal.

    - journal: the journal in question
    - author: the author of the grade
    """
    entries = Entry.objects.filter(node__journal=journal).exclude(grade=None)

    for entry in entries:
        factory.make_grade(entry, author.pk, entry.grade.grade, True)

    Comment.objects.filter(entry__node__journal=journal).exclude(entry__grade=None).update(published=True)


def send_grade_to_LMS(journal, author=None, left_journal=False, send_score=True):
    """Send grade to LMS

    If author is set, it is only for a specific author and thus the entries dont need to be updated
    """
    if author.sourcedid is None:
        return {
            'description': '{} has no sourcedid'.format(author.to_string(user=author.user)),
            'code_mayor': 'error',
        }
    if author.grade_url is None:
        return {
            'description': '{} has no grade_url'.format(author.to_string(user=author.user)),
            'code_mayor': 'error',
        }

    course = journal.assignment.get_active_course(author.user)
    if not left_journal:
        result_data = {
            'url': '{0}/Home/Course/{1}/Assignment/{2}/Journal/{3}'.format(
                settings.BASELINK, course.pk, journal.assignment.pk, journal.pk)
        }
        grade = journal.get_grade()
    else:
        result_data = {
            'url': '{0}/Home/Course/{1}/Assignment/{2}?left_journal={3}'.format(
                settings.BASELINK, course.pk, journal.assignment.pk, journal.pk)
        }
        grade = journal.get_grade() if not journal.assignment.remove_grade_upon_leaving_group else 0
    last_graded_node = journal.node_set.filter(entry__grade__published=True).order_by('entry__grade__creation_date')
    if last_graded_node.exists():
        submitted_at = str(last_graded_node.last().entry.grade.grade)
    else:
        submitted_at = None
    grade_request = GradePassBackRequest(
        author, grade, result_data=result_data, send_score=send_score,
        submitted_at=submitted_at)
    response = grade_request.send_post_request()

    return response
