from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from roster.views import views


urlpatterns = [
    path('', views.index, name='index'),
    path('browse/companies', views.CompanyList.as_view(), name='browse_companies'),
    path('signup/', views.UserSignup.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.HomePage.as_view(), name='home'),
    path('profile/settings/', views.Settings.as_view(), name='settings'),
    path('profile/<int:pk>/update/', views.UpdateProfile.as_view(), name='update_profile'),
    path('login/', LoginView.as_view(template_name='roster/login.html'), name='login'),
]