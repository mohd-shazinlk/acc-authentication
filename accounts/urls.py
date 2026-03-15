from django.urls import path
from . import views

urlpatterns = [
    path('auth/', views.login_register_view, name='login_register'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.forgot_password_view, name='forgot_password'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
] 