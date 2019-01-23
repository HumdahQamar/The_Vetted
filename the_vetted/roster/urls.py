from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from roster.views import views


urlpatterns = [
    # path('', views.index, name='index'),
    path('browse/companies', views.CompanyList.as_view(), name='browse_companies'),
    path('company/<int:pk>/add', views.company_add, name='company_add_to_rostrr'),
    path('company/<int:pk>/remove', views.company_remove, name='company_remove_from_rostrr'),
    path('company/<int:pk>/details', views.CompanyDetails.as_view(), name='company_details'),
    path('company/<int:pk>/details', views.CompanyDetails.as_view(), name='company_details'),
    path('invite/<int:invite_pk>/accept', views.accept_invite, name='accept_invite'),
    path('invite/<int:invite_pk>/reject', views.reject_invite, name='reject_invite'),
    path('signup/', views.UserSignup.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(template_name='roster/logout.html'), name='logout'),
    path('manage/companies', views.CompanyList.as_view(), name='manage_companies'),
    path('manage/users', views.UserList.as_view(), name='manage_users'),
    path('profile/', views.HomePage.as_view(), name='home'),
    path('profile/settings/', views.Settings.as_view(), name='settings'),
    path('profile/<int:pk>/update/', views.UpdateProfile.as_view(), name='update_profile'),
    path('login/', LoginView.as_view(template_name='roster/login.html'), name='login'),
    path('user/<int:user_pk>/add/<int:company_pk>', views.add_user_to_company, name='add_user_to_company'),
    path('user/<int:pk>/remove', views.remove_user_from_company, name='remove_user_from_company'),
    path('user/<int:receiver_pk>/<int:sender_pk>/invite/<int:company_pk>', views.send_invite, name='invite_user'),
    path('user/invites', views.InviteList.as_view(), name='invite_list'),
]