from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from shop.models import Profile
from django import forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email here'}))
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}))

    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name','password1','password2')


    def __init__(self,*args,**kwargs):
        super(SignUpForm, self).__init__(*args,**kwargs)
        self.fields["username"].widget.attrs["class"]="form-control"
        self.fields["username"].widget.attrs["placeholder"]="Enter a username"
        self.fields["password1"].widget.attrs["class"]="form-control"
        self.fields["password1"].widget.attrs["placeholder"]="Enter password for your account"
        self.fields["password2"].widget.attrs["class"]="form-control"
        self.fields["password2"].widget.attrs["placeholder"]="Confirm your password"



class EditUserForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email here'}))
    first_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}))
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}))
    last_login = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name', 'password', 'last_login')


class PasswordsChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new old password'}))
    new_password1 = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'}))
    new_password2 = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password again'}))

    class Meta:
        model = User
        fields = ('old_password','new_password1','new_password1')




class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))

    class Meta:
        model = User
        fields = ('username','password')


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user','bio', 'profile_picture', 'facebook_url', 'twitter_url', 'instagram_url', 'linked_in_url', 'website_url')

        widgets = {
        'user' : forms.TextInput(attrs={'class': 'form-control','value':'', 'id':'user_id', 'type':'hidden'}),
         'bio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter you biography here'}),   
         'facebook_url': forms.TextInput(attrs={'class': 'form-control'}),   
         'twitter_url': forms.TextInput(attrs={'class': 'form-control'}),   
         'instagram_url': forms.TextInput(attrs={'class': 'form-control'}),   
         'linked_in_url': forms.TextInput(attrs={'class': 'form-control'}),   
         'website_url': forms.TextInput(attrs={'class': 'form-control'}),   
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user','bio', 'profile_picture', 'facebook_url', 'twitter_url', 'instagram_url', 'linked_in_url', 'website_url')

        widgets = {
        'user' : forms.TextInput(attrs={'class': 'form-control','value':'', 'id':'user_id', 'type':'hidden'}),
         'bio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter you biography here'}),   
         'facebook_url': forms.TextInput(attrs={'class': 'form-control'}),   
         'twitter_url': forms.TextInput(attrs={'class': 'form-control'}),   
         'instagram_url': forms.TextInput(attrs={'class': 'form-control'}),   
         'linked_in_url': forms.TextInput(attrs={'class': 'form-control'}),   
         'website_url': forms.TextInput(attrs={'class': 'form-control'}),   
        }

