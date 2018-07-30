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

from django.conf import settings
from django.conf.urls.static import static

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

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('get_own_user_data/', get.get_own_user_data, name='get_own_user_data'),
    path('get_course_data/<int:cID>/', get.get_course_data, name='get_course_data'),
    path('get_assignment_data/<int:cID>/<int:aID>/', get.get_assignment_data, name='get_assignment_data'),

    path('get_user_courses/', get.get_user_courses, name='get_user_courses'),
    path('get_course_assignments/<int:cID>/', get.get_course_assignments, name='get_course_assignments'),
    path('get_assignment_journals/<int:aID>/', get.get_assignment_journals, name='get_assignment_journals'),
    path('get_journal/<int:jID>/', get.get_journal, name='get_journal'),
    path('get_upcoming_deadlines/', get.get_upcoming_deadlines, name='get_upcoming_deadlines'),
    path('get_course_permissions/<str:cID>/', get.get_course_permissions, name='get_course_permissions'),
    path('get_upcoming_course_deadlines/<int:cID>/', get.get_upcoming_course_deadlines,
         name='get_upcoming_course_deadlines'),
    path('get_nodes/<int:jID>/', get.get_nodes, name='get_nodes'),
    path('get_format/<int:aID>/', get.get_format, name='get_format'),
    path('get_names/', get.get_names, name='get_names'),
    path('get_entrycomments/<int:eID>/', get.get_entrycomments, name='get_entrycomments'),
    path('get_course_users/<int:cID>/', get.get_course_users, name='get_course_users'),
    path('get_course_roles/<int:cID>/', get.get_course_roles, name='get_user_roles'),
    path('get_user_teacher_courses/', get.get_user_teacher_courses, name='get_user_teacher_courses'),
    path('get_assignment_by_lti_id/<str:lti_id>/', get.get_assignment_by_lti_id, name='get_assignment_by_lti_id'),
    path('get_linkable_courses/', get.get_linkable_courses, name='get_linkable_courses'),
    path('get_user_data/<int:uID>/', get.get_user_data, name='get_user_data'),
    path('get_unenrolled_users/<int:cID>/', get.get_unenrolled_users, name='get_unenrolled_users'),

    path('create_new_course/', create.create_new_course, name='create_new_course'),
    path('create_new_assignment/', create.create_new_assignment, name='create_new_assignment'),
    path('create_entry/', create.create_entry, name='create_entry'),
    path('create_entrycomment/', create.create_entrycomment, name='create_entrycomment'),
    path('create_lti_user/', create.create_lti_user, name='create_lti_user'),
    path('create_journal/', create.create_journal, name='create_journal'),

    path('update_user_profile_picture/', update.update_user_profile_picture, name='update_user_profile_picture'),
    path('update_user_data/', update.update_user_data, name='update_user_data'),
    path('update_course/', update.update_course, name='update_course'),
    path('connect_course_lti/', update.connect_course_lti, name='connect_course_lti'),
    path('connect_assignment_lti/', update.connect_assignment_lti, name='connect_assignment_lti'),
    path('update_assignment/', update.update_assignment, name='update_assignment'),
    path('update_password/', update.update_password, name='update_password'),
    path('update_grade_notification/', update.update_grade_notification,
         name='update_grade_notification'),
    path('update_comment_notification/', update.update_comment_notification,
         name='update_comment_notification'),
    path('update_format/', update.update_format, name='update_format'),
    path('update_entrycomment/', update.update_entrycomment, name='update_entrycomment'),
    path('update_lti_id_to_user/', update.update_lti_id_to_user, name='update_lti_id_to_user'),
    path('update_course_roles/', update.update_course_roles, name='update_course_roles'),

    path('update_grade_entry/', update.update_grade_entry, name='update_grade_entry'),
    path('update_publish_grade_entry/', update.update_publish_grade_entry, name='update_grade_entry'),
    path('update_publish_grades_assignment/', update.update_publish_grades_assignment,
         name='update_publish_grades_assignment'),
    path('update_publish_grades_journal/', update.update_publish_grades_journal,
         name='update_publish_grades_journal'),
    path('update_user_role_course/', update.update_user_role_course, name='update_user_role_course'),
    path('update_course_with_student/', update.update_course_with_student, name='update_course_with_student'),

    path('delete_course/', delete.delete_course, name='delete_course'),
    path('delete_assignment/', delete.delete_assignment, name='delete_assignment'),
    path('delete_user_from_course/', delete.delete_user_from_course, name='delete_user_from_course'),
    path('delete_course_role/', delete.delete_course_role, name='delete_course_role'),

    path('lti/launch', get.lti_launch, name='lti_launch'),
    path('get_lti_params_from_jwt/<str:jwt_params>/', get.get_lti_params_from_jwt, name='get_lti_params_from_jwt'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
