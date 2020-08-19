from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from shop.models import Profile
from django.contrib.auth import authenticate
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.urls import reverse_lazy, reverse
from .forms import SignUpForm, EditUserForm, PasswordsChangeForm, MyAuthenticationForm, CreateProfileForm, EditProfileForm
from django.http import HttpResponseRedirect


def PasswordSuccessView(request):
    return render(request, 'registration/password_success.html', {})

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordsChangeForm
    success_url = reverse_lazy("members:password_success")

class MyLoginView(LoginView):
    form_class = MyAuthenticationForm

class UserRegisterView(CreateView):
    form_class = SignUpForm
    template_name = "registration/register.html"
    success_url = reverse_lazy('members:login')

class UserEditView(UpdateView):
    
    form_class = EditUserForm
    template_name = "registration/edit_settings.html"
    success_url = reverse_lazy('shop:shop')

    def get_object(self):
        return self.request.user


def ShowProfile(request):
    return render(request, 'registration/profile.html',{})


class ProfileCreateView(CreateView):
    form_class = CreateProfileForm
    template_name = "registration/create_profile.html"
    success_url = reverse_lazy('shop:shop')

class ProfileEditView(UpdateView):
    model = Profile
    template_name = 'registration/edit_profile.html'
    form_class = EditProfileForm
    success_url = reverse_lazy('shop:shop')