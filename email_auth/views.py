from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from email_auth.forms import RegistrationForm, LoginForm, ChangeForm
from email_auth.verify import Verification
from django.contrib.auth.models import User


class IndexView(View):
    index_template = 'index.html'

    def get(self, request):
        context = {}
        if request.user.is_authenticated():
            user = get_object_or_404(User, username=request.user.username)
            context['user_id'] = user.id
        context['content'] = "This is secret content"
        context['message'] = "Only verificated users can see secret content"
        return render(request, self.index_template, context)

    @staticmethod
    def post(request):
        return HttpResponseNotFound('<h1>Page not found</h1>')


class RegistrationView(View):
    success_url_redirect = '/'
    registration_template = 'registration_form.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.registration_template,
                      {'registration_form': form})

    def post(self, request):
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            verify = Verification()
            user = form.save()
            user.is_active = False
            verify.send_login_data(user, user.password)
            user.set_password(user.password)
            user.save()
            login(request, user)
            verify.send_verify_message(user)
            return HttpResponseRedirect(self.success_url_redirect)
        else:
            return render(request, self.registration_template,
                          {'registration_form': form,
                           'errors': form.errors})


class LogoutView(View):
    logout_redirect_url = '/'

    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(self.logout_redirect_url)

    @staticmethod
    def post(request):
        return HttpResponseNotFound('<h1>Page not found</h1>')


class LoginView(View):
    login_redirect_url = '/'
    login_template = 'login_form.html'
    form = LoginForm()

    def get(self, request):
        return render(request, self.login_template,
                      {'login_form': self.form})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)

        else:
            return render(request, self.login_template,
                          {'login_form': self.form,
                           'message': "Invalid login details."})
        return HttpResponseRedirect(self.login_redirect_url)


class ChangeView(View):
    change_redirect_url = '/'
    change_user_template = 'change_user.html'

    def get(self, request, user_id):
        if request.user.is_authenticated():
            user = get_object_or_404(User, id=user_id)
            data = {'username': user.username,
                    'email': user.email}
            change_form = ChangeForm(initial=data)
            return render(request, self.change_user_template,
                          {'change_user_form': change_form})
        else:
            return HttpResponseNotFound('<h1>Page not found</h1>')

    def post(self, request, user_id):
        form = ChangeForm(data=request.POST)
        user = User.objects.get(id=user_id)
        password = request.POST['password']
        user = authenticate(username=user.username, password=password)
        if user:
            user.username = request.POST['username']
            user.email = request.POST['email']
            if request.POST['new_password']:
                if request.POST['new_password'] == request.POST['repeat_new_password']:
                    user.set_password(request.POST['new_password'])
                    password = request.POST['new_password']

            user.save()
            verify = Verification()
            verify.send_login_data(user, password)
            login(request, user)
            return HttpResponseRedirect(self.change_redirect_url)

        else:
            return render(request, self.change_user_template,
                          {'change_user_form': form,
                           'errors': 'Incorrect password !'})
