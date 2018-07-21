from rest_framework import routers
from VLE.views.course import CourseView
from VLE.views.role import RoleView
from VLE.views.user import UserView
from VLE.views.assignment import AssignmentView
from VLE.views.node import NodeView
from VLE.views.comment import CommentView
from VLE.views.participation import ParticipationView

router = routers.DefaultRouter()
router.register(r'courses', CourseView, base_name='course')
router.register(r'roles', RoleView, base_name='role')
router.register(r'users', UserView, base_name='user')
router.register(r'assignments', AssignmentView, base_name='assignment')
router.register(r'nodes', NodeView, base_name='node')
router.register(r'comments', CommentView, base_name='comment')
router.register(r'participations', ParticipationView, base_name='participation')

urlpatterns = router.urls
