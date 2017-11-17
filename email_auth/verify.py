import requests
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.http import int_to_base36, base36_to_int
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User


class Verification(object):
    email_api_url = "https://api.mailgun.net/v3/sandbox268cbe1e4d2b464985c8aa6582d420d9.mailgun.org/messages"
    email_api_key = "key-a1232d52f2be42631a4f568a8edfa6e4"
    email_sender = "Test email Verification <postmaster@sandbox268cbe1e4d2b464985c8aa6582d420d9.mailgun.org>"

    @staticmethod
    def get_verify_url(user):
        token = default_token_generator.make_token(user)
        user_id = int_to_base36(user.id)
        url = reverse('confirm_register', args=(user_id, token))
        return url

    @staticmethod
    def confirm_register(request, user_id_b36, token):
        try:
            user_id_int = base36_to_int(user_id_b36)
        except ValueError:
            raise Http404('Verification error: Wrong user id')

        user = get_object_or_404(User, id=user_id_int)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index_page'))
        else:
            raise Http404('Verification error: Token error')

    def send_verify_message(self, user):
        url = self.get_verify_url(user)
        return requests.post(
            self.email_api_url,
            auth=("api", self.email_api_key),
            data={"from": self.email_sender,
                  "to": [user.email],
                  "subject": "Email Verification",
                  "text": "For verification follow this link: http://127.0.0.1:8000" + url})

    @staticmethod
    def send_verify_again(request):
        if request.user.is_authenticated():
            user_name = request.user.username
            user = get_object_or_404(User, username=user_name)
            verify = Verification()
            verify.send_verify_message(user)
            return HttpResponseRedirect(reverse('index_page'))

    def send_login_data(self, user, password):
        return requests.post(
            self.email_api_url,
            auth=("api", self.email_api_key),
            data={"from": self.email_sender,
                  "to": [user.email],
                  "subject": "Test login information",
                  "text": "Login information:\n" +
                          " --login/username: {0} \n".format(user.username) +
                          " --email: {0} \n".format(user.email) +
                          " --password: {0}".format(password)
                  })
