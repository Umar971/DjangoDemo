from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

app_name = "members"
urlpatterns = [
    # register is our defined route
    path('register/', views.UserRegisterView.as_view(), name='register'),
    # login and logout here are redirecting to the django built-in pre defined views
    path('login/', views.MyLoginView.as_view(), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # change password from built-in django views
    # path('password/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html')),
    # edit profile url
    path('edit_settings/', views.UserEditView.as_view(), name='edit_settings'),
    path('edit_profile/<int:pk>', views.ProfileEditView.as_view(), name='edit_profile'),
    path('password_success/', views.PasswordSuccessView, name='password_success'),
# in custon view
    path('password/', views.PasswordsChangeView.as_view(template_name='registration/change-password.html')),
    path('show_profile/', views.ShowProfile, name='show_profile'),
    path('create_profile/', views.ProfileCreateView.as_view(), name='create_profile'),



]
