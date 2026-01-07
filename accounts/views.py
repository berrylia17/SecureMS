from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random

from .forms import RegisterForm, ProfileUpdateForm   # your custom forms


# Utility: generate MFA code
def generate_mfa_code():
    return str(random.randint(100000, 999999))


# Register new user
from django.core.mail import send_mail

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Send welcome email
            send_mail(
                subject="Welcome to SecureMS!",
                message="Thank you for registering. Your account has been created successfully.",
                from_email="no-reply@securems.com",
                recipient_list=[user.email],
                fail_silently=False,
            )

            messages.success(request, "Account created successfully. Please log in.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})



# Login with MFA
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            # Step 1: generate MFA code
            code = generate_mfa_code()
            request.session['mfa_code'] = code
            request.session['pending_user_id'] = user.id

            # Step 2: send code via email (console backend prints it in dev mode)
            send_mail(
                'Your SecureMS MFA Code',
                f'Your login code is: {code}',
                'securems@example.com',
                [user.email],
                fail_silently=False,
            )

            # Step 3: redirect to MFA verification page
            return redirect("mfa_verify")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "accounts/login.html")


# MFA verification
def mfa_verify_view(request):
    if request.method == "POST":
        entered_code = request.POST.get("code")
        if entered_code == request.session.get("mfa_code"):
            user_id = request.session.get("pending_user_id")
            user = User.objects.get(id=user_id)
            login(request, user)
            messages.success(request, "Login successful with MFA.")
            # Redirect to home.html
            return redirect("home")  
        else:
            messages.error(request, "Invalid MFA code.")
    return render(request, "accounts/mfa_verify.html")



# Logout user
def logout_view(request):
    logout(request)
    return redirect("home")   # safer than hardcoding "/"


# Edit user profile
@login_required
def edit_profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("edit_profile")
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, "accounts/edit_profile.html", {"form": form})


# Change password
@login_required
def change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keep user logged in
            messages.success(request, "Password changed successfully.")
            return redirect("change_password")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "accounts/change_password.html", {"form": form})
