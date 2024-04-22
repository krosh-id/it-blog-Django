from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import RegisterUserForm, LoginUserForm


# Create your views here.
class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'


def login(request):
    return render(request, "users/login.html")


def logout(request):
    return render(request, "users/login.html")


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')