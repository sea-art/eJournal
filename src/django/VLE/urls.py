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
from django.conf.urls import url, include
from django.urls import path

from VLE.views import common, lti, email

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    # TokenVerifyView,
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^', include(('VLE.views.urls', 'VLE.views'), namespace='VLE')),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('forgot_password/', email.forgot_password, name='forgot_password'),
    path('recover_password/', email.recover_password, name='recover_password'),
    path('verify_email/', email.verify_email, name='verify_email'),
    path('request_email_verification/', email.request_email_verification, name='request_email_verification'),

    path('lti/launch', lti.lti_launch, name='lti_launch'),
    path('get_lti_params_from_jwt/<str:jwt_params>/', lti.get_lti_params_from_jwt, name='get_lti_params_from_jwt'),

    path('names/<int:course_id>/<int:assignment_id>/<int:journal_id>/', common.names, name='names'),
]

# if settings.DEBUG is True:
#      urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
