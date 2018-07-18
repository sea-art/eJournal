from rest_framework import routers
from VLE.views.course import CourseView
from VLE.views.user import UserView
from VLE.views.assignment import AssignmentView
from VLE.views.node import NodeView
from VLE.views.comment import CommentView

router = routers.DefaultRouter()
router.register(r'courses', CourseView, base_name='course')
router.register(r'users', UserView, base_name='user')
router.register(r'assignments', AssignmentView, base_name='assignment')
router.register(r'nodes', NodeView, base_name='node')
router.register(r'comments', CommentView, base_name='comment')

urlpatterns = router.urls
