from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from roster.views import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.UserSignup.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='roster/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]