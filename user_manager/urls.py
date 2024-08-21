from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from user_manager.views.auth_view import UserLoginView, UserRegisterView
from user_manager.views.web_view import home_view, contact_view
from user_manager.views.render_view import render_project
from user_manager.views.error_view import custom_404_view
from user_manager.views.dashboard_views import dashboard_view, logout_view
from user_manager.views.domain_views import domain_list, domain_create, domain_update, domain_delete, file_manager_view
from user_manager.views.member_view import member_delete, member_list


urlpatterns = [
    path('', render_project, name='home'),
    path('contact/', contact_view, name='contact'),
    path('login/', UserLoginView.as_view(), name='account_login'),
    path('register/', UserRegisterView.as_view(), name='account_register'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html'), name='account_password_reset'),
    path('logout/', logout_view, name='logout'),
    # DASHBOARD
    path('dashboard/', dashboard_view, name='dashboard'),
    # DASHBOARD MEMBER
    path('dashboard/account/', member_list, name='member_list'),
    path('dashboard/account/delete/<int:pk>/', member_delete, name='member_delete'),
    # DASHBOARD DOMAINS
    path('dashboard/domains/', domain_list, name='domain_list'),
    path('dashboard/domains/create/', domain_create, name='domain_create'),
    path('dashboard/domains/<int:pk>/edit/', domain_update, name='domain_update'),
    path('dashboard/domains/<int:pk>/delete/', domain_delete, name='domain_delete'),
    path('dashboard/files/', file_manager_view, name='file_manager'),


]

handler404 = custom_404_view
