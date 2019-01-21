from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from roster.views import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.UserSignup.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='roster/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/landing/', views.LandingPage.as_view(), name='landing'),
    path('profile/settings/', views.Settings.as_view(), name='settings'),
    path('profile/<int:pk>/update/', views.UpdateProfile.as_view(), name='update_profile'),
]