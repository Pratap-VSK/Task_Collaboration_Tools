from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import UserProfile
from .forms import ProfileEditForm, AccountDeleteForm, CustomSignupForm
from django.contrib.auth.models import User


def custom_signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('dashboard')
    else:
        form = CustomSignupForm()

    context = {'form': form, 'page_title': 'Sign Up'}
    return render(request, 'account/signup.html', context)


@login_required
def settings_view(request):
    user_profile = request.user.userprofile
    context = {
        'user_profile': user_profile,
        'page_title': 'Settings'
    }
    return render(request, 'accounts/settings.html', context)


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('settings')
    else:
        form = ProfileEditForm(instance=request.user)

    context = {
        'form': form,
        'page_title': 'Edit Profile'
    }
    return render(request, 'accounts/profile_edit.html', context)


@login_required
def account_delete_view(request):
    if request.method == 'POST':
        form = AccountDeleteForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.user.username, password=form.cleaned_data['password'])
            if user is not None:
                user.delete()
                messages.success(request, 'Account deleted successfully!')
                return redirect('login')
            else:
                messages.error(request, 'Invalid password. Please try again.')
    else:
        form = AccountDeleteForm()

    context = {
        'form': form,
        'page_title': 'Delete Account'
    }
    return render(request, 'accounts/account_confirm_delete.html', context)


@login_required
@require_POST
def change_theme(request):
    user_profile = request.user.userprofile

    if 'theme_mode' in request.POST:
        theme_mode = request.POST.get('theme_mode')
        if theme_mode in ['light', 'dark']:
            user_profile.theme_mode = theme_mode
            user_profile.save()

    if 'color_scheme' in request.POST:
        color_scheme = request.POST.get('color_scheme')
        valid_colors = ['blue', 'purple', 'green', 'orange', 'pink', 'indigo']
        if color_scheme in valid_colors:
            user_profile.color_scheme = color_scheme
            user_profile.save()

    # Redirect to referrer or dashboard
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
