from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import random

from .forms import RegistrationForm, LoginForm, ForgotPasswordForm, OTPVerificationForm, SetNewPasswordForm
from .models import OneTimePassword

def login_register_view(request):
    login_form = LoginForm(request.POST or None)
    register_form = RegistrationForm(request.POST or None)
    
    if 'login_submit' in request.POST:
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            
            # Since username is email, we first get the user object by email
            user_obj = User.objects.filter(email=email).first()
            
            if user_obj:
                # If user exists, we authenticate with their username
                user = authenticate(request, username=user_obj.username, password=password)
                if user:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid credentials.')
            else:
                # If user object does not exist, the email is not registered
                messages.error(request, 'Email not registered.')

    if 'register_submit' in request.POST:
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            # Send welcome email
            send_mail(
                'Welcome to devWebApp!',
                'Thank you for registering. Your account has been created successfully.',
                'noreply@devwebapp.com',
                [user.email],
                fail_silently=False,
            )
            return redirect('profile') # Redirect to profile page

    context = {
        'login_form': login_form,
        'register_form': register_form,
    }
    return render(request, 'accounts/login_register.html', context)

def logout_view(request):
    logout(request)
    return redirect('login_register')

def forgot_password_view(request):
    form = ForgotPasswordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data.get('email')
        user = User.objects.get(email=email)
        
        # Generate OTP
        otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        OneTimePassword.objects.update_or_create(
            user=user, defaults={'otp': otp_code}
        )
        
        # Send OTP email
        send_mail(
            'Password Reset OTP',
            f'Your OTP for password reset is: {otp_code}. It is valid for 1 minute.',
            'shazinlk555@gmail.com',
            [user.email],
            fail_silently=False,
        )
        
        # Store email in session to use in the next step
        request.session['password_reset_email'] = email
        messages.success(request, 'OTP has been sent to your email.')
        return redirect('verify_otp')

    return render(request, 'accounts/forgot_password.html', {'form': form})

def verify_otp_view(request):
    form = OTPVerificationForm(request.POST or None)
    email = request.session.get('password_reset_email')
    if not email:
        messages.error(request, 'Something went wrong. Please try again.')
        return redirect('forgot_password')

    if request.method == 'POST' and form.is_valid():
        user = User.objects.get(email=email)
        otp_instance = OneTimePassword.objects.filter(user=user).first()
        
        if otp_instance and otp_instance.otp == form.cleaned_data.get('otp'):
            # Check if OTP is expired (1 minute validity)
            if timezone.now() - otp_instance.created_at > timedelta(minutes=1):
                messages.error(request, 'OTP has expired. Please request a new one.')
                otp_instance.delete()
                return redirect('forgot_password')
            
            # OTP is valid
            request.session['otp_verified'] = True
            otp_instance.delete() # OTP is used, so delete it
            return redirect('reset_password')
        else:
            messages.error(request, 'Invalid OTP.')
            
    return render(request, 'accounts/otp_verify.html', {'form': form})

def reset_password_view(request):
    if not request.session.get('otp_verified'):
        messages.error(request, 'Please verify your OTP first.')
        return redirect('forgot_password')

    form = SetNewPasswordForm(request.POST or None)
    email = request.session.get('password_reset_email')
    
    if request.method == 'POST' and form.is_valid():
        user = User.objects.get(email=email)
        new_password = form.cleaned_data.get('new_password')
        user.set_password(new_password)
        user.save()
        
        # Clear session data
        del request.session['password_reset_email']
        del request.session['otp_verified']
        
        # Send confirmation email
        send_mail(
            'Password Reset Successful',
            'Your password has been reset successfully.',
            'noreply@devwebapp.com',
            [user.email],
            fail_silently=False,
        )
        
        messages.success(request, 'Password has been reset successfully. You can now login.')
        return redirect('login_register')

    return render(request, 'accounts/reset_password.html', {'form': form})

# I will add the other views in subsequent steps.
