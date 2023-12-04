from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
import os
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users-login')
    else:
        form = SignUpForm()
    context = {
        'form': form,
    }
    return render(request, 'users/sign_up.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            try:
                profile = request.user.profilemodel  # Attempt to get the profile
                p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            except ObjectDoesNotExist:
                # If profile doesn't exist, create a new instance
                p_form = ProfileUpdateForm(request.POST, request.FILES)

            if p_form.is_valid():
                profile_instance = p_form.save(commit=False)
                profile_instance.user = request.user
                profile_instance.save()
                return redirect('users-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        try:
            profile = request.user.profilemodel
            p_form = ProfileUpdateForm(instance=profile)
        except ObjectDoesNotExist:
            p_form = ProfileUpdateForm()  # Create a new form instance

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)
