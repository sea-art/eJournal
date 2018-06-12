from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.http import JsonResponse, HttpResponse


@api_view(['GET'])
def test(request, format=None):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)

    return JsonResponse({'result': 'success',
                         'user': request.user.username})
