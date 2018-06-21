"""VLE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from VLE.views.get import lti_launch
from VLE.views.get import lti_grade_replace_result

from VLE.views.get import get_own_user_data
from VLE.views.get import get_course_data
from VLE.views.get import get_assignment_data

from VLE.views.get import get_user_courses
from VLE.views.get import get_course_assignments
from VLE.views.get import get_assignment_journals
from VLE.views.get import get_upcoming_deadlines
from VLE.views.get import get_nodes
from VLE.views.get import get_format
from VLE.views.get import get_names
from VLE.views.get import get_course_users

from VLE.views.create import create_new_course
from VLE.views.create import create_new_assignment
from VLE.views.create import create_entry

from VLE.views.update import update_course
from VLE.views.update import update_assignment
from VLE.views.update import update_password
from VLE.views.update import update_grade_notification
from VLE.views.update import update_comment_notification

from VLE.views.update import update_grade_entry
from VLE.views.update import update_publish_grade_entry
from VLE.views.update import update_publish_grades_assignment
from VLE.views.update import update_publish_grades_journal

from VLE.views.delete import delete_course
from VLE.views.delete import delete_assignment

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/get_own_user_data/', get_own_user_data, name='get_own_user_data'),
    path('api/get_course_data/<int:cID>/', get_course_data, name='get_course_data'),
    path('api/get_assignment_data/<int:cID>/<int:aID>/', get_assignment_data, name='get_assignment_data'),

    path('api/get_user_courses/', get_user_courses, name='get_user_courses'),
    path('api/get_course_assignments/<int:cID>/', get_course_assignments, name='get_course_assignments'),
    path('api/get_assignment_journals/<int:aID>/', get_assignment_journals, name='get_assignment_journals'),
    path('api/get_upcoming_deadlines/', get_upcoming_deadlines, name='get_upcoming_deadlines'),
    path('api/get_nodes/<int:jID>/', get_nodes, name='get_nodes'),
    path('api/get_format/<int:aID>/', get_format, name='get_format'),
    path('api/get_names/', get_names, name='get_names'),
    path('api/get_course_users/<int:cID>/', get_course_users, name='get_course_users'),

    path('api/create_new_course/', create_new_course, name='create_new_course'),
    path('api/create_new_assignment/', create_new_assignment, name='create_new_assignment'),
    path('api/create_entry/', create_entry, name='create_entry'),

    path('api/update_course/', update_course, name='update_course'),
    path('api/update_assignment/', update_assignment, name='update_assignment'),
    path('api/update_password/', update_password, name='update_password'),
    path('api/update_grade_notification/', update_grade_notification,
         name='update_grade_notification'),
    path('api/update_comment_notification/', update_comment_notification,
         name='update_comment_notification'),

    path('api/update_grade_entry/<int:eID>/', update_grade_entry, name='update_grade_entry'),
    path('api/update_publish_grade_entry/<int:eID>/', update_publish_grade_entry, name='update_grade_entry'),
    path('api/update_publish_grades_assignment/<int:aID>/', update_publish_grades_assignment,
         name='update_publish_grades_assignment'),
    path('api/update_publish_grades_journal/<int:jID>/', update_publish_grades_journal,
         name='update_publish_grades_journal'),

    path('api/delete_course/', delete_course, name='delete_course'),
    path('api/delete_assignment/', delete_assignment, name='delete_assignment'),

    path('api/lti/launch', lti_launch, name='lti_launch'),
]
