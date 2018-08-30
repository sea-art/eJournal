from rest_framework import routers
from VLE.views.course import CourseView
from VLE.views.role import RoleView
from VLE.views.user import UserView
from VLE.views.assignment import AssignmentView
from VLE.views.node import NodeView
from VLE.views.comment import CommentView
from VLE.views.participation import ParticipationView
from VLE.views.journal import JournalView
from VLE.views.journalformat import JournalFormatView
from VLE.views.entry import EntryView
from VLE.views.journalformat import JournalFormatView

router = routers.DefaultRouter()
router.register(r'courses', CourseView, base_name='course')
router.register(r'roles', RoleView, base_name='role')
router.register(r'users', UserView, base_name='user')
router.register(r'assignments', AssignmentView, base_name='assignment')
router.register(r'nodes', NodeView, base_name='node')
router.register(r'comments', CommentView, base_name='comment')
router.register(r'participations', ParticipationView, base_name='participation')
router.register(r'journals', JournalView, base_name='journal')
router.register(r'entries', EntryView, base_name='entry')
router.register(r'journalformats', JournalFormatView, base_name='journalformat')

urlpatterns = router.urls
