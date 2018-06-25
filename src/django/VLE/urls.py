"""
VLE URL Configuration.

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

import VLE.views.get as get
import VLE.views.create as create

import VLE.views.update as update

import VLE.views.delete as delete

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

    path('api/get_own_user_data/', get.get_own_user_data, name='get_own_user_data'),
    path('api/get_course_data/<int:cID>/', get.get_course_data, name='get_course_data'),
    path('api/get_assignment_data/<int:cID>/<int:aID>/', get.get_assignment_data, name='get_assignment_data'),

    path('api/get_user_courses/', get.get_user_courses, name='get_user_courses'),
    path('api/get_course_assignments/<int:cID>/', get.get_course_assignments, name='get_course_assignments'),
    path('api/get_assignment_journals/<int:aID>/', get.get_assignment_journals, name='get_assignment_journals'),
    path('api/get_upcoming_deadlines/', get.get_upcoming_deadlines, name='get_upcoming_deadlines'),
    path('api/get_course_permissions/<str:cID>/', get.get_course_permissions, name='get_course_permissions'),
    path('api/get_nodes/<int:jID>/', get.get_nodes, name='get_nodes'),
    path('api/get_format/<int:aID>/', get.get_format, name='get_format'),
    path('api/get_names/', get.get_names, name='get_names'),
    path('api/get_entrycomments/<int:entryID>/', get.get_entrycomments, name='get_entrycomments'),
    path('api/get_course_users/<int:cID>/', get.get_course_users, name='get_course_users'),
    path('api/get_template/<int:tID>/', get.get_template, name='get_template'),
    path('api/get_unenrolled_users/<int:cID>/', get.get_unenrolled_users, name='get_unenrolled_users'),

    path('api/create_new_course/', create.create_new_course, name='create_new_course'),
    path('api/create_new_assignment/', create.create_new_assignment, name='create_new_assignment'),
    path('api/create_entry/', create.create_entry, name='create_entry'),
    path('api/create_entrycomment/', create.create_entrycomment, name='create_entrycomment'),

    path('api/update_user_data/', update.update_user_data, name='update_user_data'),
    path('api/update_course/', update.update_course, name='update_course'),
    path('api/update_assignment/', update.update_assignment, name='update_assignment'),
    path('api/update_password/', update.update_password, name='update_password'),
    path('api/update_grade_notification/', update.update_grade_notification,
         name='update_grade_notification'),
    path('api/update_comment_notification/', update.update_comment_notification,
         name='update_comment_notification'),
    path('api/update_format/', update.update_format, name='update_format'),
    path('api/update_entrycomment/', update.update_entrycomment, name='update_entrycomment'),

    path('api/update_grade_entry/<int:eID>/', update.update_grade_entry, name='update_grade_entry'),
    path('api/update_publish_grade_entry/<int:eID>/', update.update_publish_grade_entry, name='update_grade_entry'),
    path('api/update_publish_grades_assignment/<int:aID>/', update.update_publish_grades_assignment,
         name='update_publish_grades_assignment'),
    path('api/update_publish_grades_journal/<int:jID>/', update.update_publish_grades_journal,
         name='update_publish_grades_journal'),
    path('api/update_user_role_course/', update.update_user_role_course, name='update_user_role_course'),
    path('api/update_course_with_studentID/', update.update_course_with_studentID, name='update_course_with_studentID'),


    path('api/delete_course/', delete.delete_course, name='delete_course'),
    path('api/delete_assignment/', delete.delete_assignment, name='delete_assignment'),
    path('api/delete_user_from_course/', delete.delete_user_from_course, name='delete_user_from_course'),

    path('api/lti/launch', get.lti_launch, name='lti_launch'),
]
