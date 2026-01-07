from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
import random
import logging

from .forms import RegisterForm, ProfileUpdateForm   # your custom forms
from ratelimit.decorators import ratelimit

# Logger for accounts app
logger = logging.getLogger('accounts')


# Utility: generate MFA code
def generate_mfa_code():
    return str(random.randint(100000, 999999))


# Register new user
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
            # Log invalid attempts for audit trail
            for field, errors in form.errors.items():
                for error in errors:
                    logger.warning(
                        f"Invalid input on registration: field={field}, error={error}, ip={request.META.get('REMOTE_ADDR')}, path={request.path}"
                    )
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


# Login with MFA (rate limited: 5 attempts/minute per IP)
@ratelimit(key='ip', rate='5/m', block=True)
def login_view(request):
    if getattr(request, 'limited', False):
        messages.error(request, "Too many login attempts. Please wait before trying again.")
        return render(request, "accounts/login.html")

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
            logger.warning(
                f"Invalid login attempt: username={username}, ip={request.META.get('REMOTE_ADDR')}, path={request.path}"
            )
            messages.error(request, "Invalid username or password.")
    return render(request, "accounts/login.html")


# MFA verification (rate limited: 3 attempts/minute per IP)
@ratelimit(key='ip', rate='3/m', block=True)
def mfa_verify_view(request):
    if getattr(request, 'limited', False):
        messages.error(request, "Too many MFA attempts. Please wait before trying again.")
        return render(request, "accounts/mfa_verify.html")

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
            logger.warning(
                f"Invalid MFA attempt: code={entered_code}, ip={request.META.get('REMOTE_ADDR')}, path={request.path}"
            )
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
            for field, errors in form.errors.items():
                for error in errors:
                    logger.warning(
                        f"Invalid profile update: field={field}, error={error}, user={request.user.username}, ip={request.META.get('REMOTE_ADDR')}, path={request.path}"
                    )
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
            for field, errors in form.errors.items():
                for error in errors:
                    logger.warning(
                        f"Invalid password change: field={field}, error={error}, user={request.user.username}, ip={request.META.get('REMOTE_ADDR')}, path={request.path}"
                    )
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "accounts/change_password.html", {"form": form})


# Isolated test view for rate limiting
@ratelimit(key='ip', rate='2/m', block=True)
def test_view(request):
    if getattr(request, 'limited', False):
        logger.warning(
            f"Rate limit exceeded: ip={request.META.get('REMOTE_ADDR')}, path={request.path}"
        )
        return HttpResponse("Rate limit exceeded", status=429)
    return HttpResponse("OK")
