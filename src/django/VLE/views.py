from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.http import JsonResponse


@api_view(['GET'])
def test(request, format=None):
    return JsonResponse({'result': 'success',
                         'user': request.user.username})
