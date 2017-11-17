"""email_auth_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from email_auth import views, verify

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.IndexView.as_view(), name='index_page'),
    url(r'^auth/register/$', views.RegistrationView.as_view(), name='register_page'),
    url(r'^auth/login/$', views.LoginView.as_view(), name='login_page'),
    url(r'^auth/logout/$', views.LogoutView.as_view(), name='logout_page'),
    url(r'^auth/change/(?P<user_id>[\w\-]+)/$', views.ChangeView.as_view(), name='change_page'),
    url(r'^auth/confirm/send/$', verify.Verification.send_verify_again,
        name='send_verify_again'),
    url(r'^auth/confirm/([\w\-]+)/([\w\-]+)/$', verify.Verification.confirm_register,
        name='confirm_register'),
]
