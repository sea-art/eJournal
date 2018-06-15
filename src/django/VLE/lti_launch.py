from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from urllib.parse import quote
import oauth2
import json
import pprint as pprint

from .models import User


class OAuthRequestValidater(object):
    """
    OAuth request validater Django
    """

    def __init__(self, key, secret):
        super(OAuthRequestValidater, self).__init__()
        self.consumer_key = key
        self.consumer_secret = secret

        self.oauth_server = oauth2.Server()
        signature_method = oauth2.SignatureMethod_HMAC_SHA1()
        self.oauth_server.add_signature_method(signature_method)
        self.oauth_consumer = oauth2.Consumer(
            self.consumer_key, self.consumer_secret
        )

    def parse_request(self, request):
        headers = dict([(k, request.META[k])
                        for k in request.META if
                        k.upper().startswith('HTTP_') or
                        k.upper().startswith('CONTENT_')])

        return request.method, request.build_absolute_uri(), headers, request.POST

    def is_valid(self, request):
        try:
            method, url, head, param = self.parse_request(request)

            oauth_request = oauth2.Request.from_request(
                method, url, headers=head, parameters=(param))

            oauth_request = oauth2.Request.from_request(
                request.method, request.build_absolute_uri(),
                headers=request.META, parameters=request.POST.dict()
            )
            self.oauth_server.verify_request(oauth_request,
                                             self.oauth_consumer, {})

        except (oauth2.Error, ValueError) as err:
            print(oauth_request["oauth_signature"])
            oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), self.oauth_consumer, {})
            print(oauth_request["oauth_signature"])
            return False, err
        # Signature was valid
        return True, None


def check_signature(key, secret, request):
    """
    Validates OAuth request using the python-oauth2 library:
        https://github.com/simplegeo/python-oauth2.
    """
    validator = OAuthRequestValidater(key, secret)
    return validator.is_valid(request)


def createNewUser(request):
    user = User()
    if "lis_person_contact_email_primary" in request.POST:
        user.email = request.POST["lis_person_contact_email_primary"]

    if "lis_person_sourcedid" in request.POST:
        user.username = request.POST["lis_person_sourcedid"]

    user.lti_id = lti_user_id
    user.save()
    return user


@csrf_exempt
@xframe_options_exempt
def lti_launch(request):
    if request.method == "POST":
        # canvas
        secret = "4339900ae5861f3086861ea492772864"
        key = "0cd500938a8e7414ccd31899710c98ce"

        # # tutorial
        # secret = "85c6d62c8684f0ff4f3ad49166a4e387"
        # key = "b25d130af472a09c9d5897587b7f387f"

        print("key = postkey", key == request.POST["oauth_consumer_key"])
        authicated, err = check_signature(key, secret, request)

        if authicated:
            lti_user_id = request.POST["user_id"]

            users = User.objects.filter(lti_id=lti_user_id)
            if users.count() > 0:
                user = users[0]
            else:
                user = createNewUser(request)

            token = TokenObtainPairSerializer.get_token(user)
            access = token.access_token
            response = {'result': 'success'}
            status = 200
            return redirect('http://localhost:8080/#/lti/launch?jwt_refresh={0}&jwt_access={1}'.format(token, access))

        else:
            response = {'error': '401 Authentication Error'}
            status = 401
            return HttpResponse("unsuccesfull auth, {0}".format(err))

        # # Tutorial code not needed
        # redir = False
        # if redir:
        #     # redirect with lti_errorlog
        #     if "launch_presentation_return_url" in request.POST:
        #         # Parameter to set start of parameters by checking if there are
        #         # already parameters in string
        #         startparam = "&" if "?" in request.POST["launch_presentation_return_url"] else "?"
        #
        #         # creates safe urls (& is not seen as new param)
        #         param = "lti_errorlog="
        #         param += quote("The floor's on fire... see... *&* the chair.", safe='')
        #
        #         return redirect(request.POST["launch_presentation_return_url"]+startparam+param)
        #
        #     # redirect with lti_errormsg
        #     if "launch_presentation_return_url" in request.POST:
        #         # Parameter to set start of parameters by checking if there are
        #         # already parameters in string
        #         startparam = "&" if "?" in request.POST["launch_presentation_return_url"] else "?"
        #         return redirect(request.POST["launch_presentation_return_url"]+startparam+"lti_errormsg=Who's going to save you, Junior?!")
        #
        #
        #     # redirect with lti_log
        #     if "launch_presentation_return_url" in request.POST:
        #         # Parameter to set start of parameters by checking if there are
        #         # already parameters in string
        #         startparam = "&" if "?" in request.POST["launch_presentation_return_url"] else "?"
        #         return redirect(request.POST["launch_presentation_return_url"]+startparam+"lti_log=One ping only.")
        #
        #     # redirect with lti_msg
        #     if "launch_presentation_return_url" in request.POST:
        #         return redirect(request.POST["launch_presentation_return_url"]+"?lti_msg=Most things in here don't react well to bullets.")
        #
        #     # blank redirect
        #     if "launch_presentation_return_url" in request.POST:
        #         return redirect(request.POST["launch_presentation_return_url"])

        # Prints de post parameters als http page
        post = json.dumps(request.POST, separators=(',', ': '))
        return HttpResponse(post.replace(",", " <br> "))

    return HttpResponse("Hello, world. You're at the polls index.")
