from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserAuth
from .forms import RegistrationForm
import requests
from bs4 import BeautifulSoup
from django.db.models import Avg
import json
import datetime


def main(request):
    return render(request, 'main/main.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()

            try:
                user_auth = UserAuth.objects.get(user=user)
            except UserAuth.DoesNotExist:
                user_auth = UserAuth(user=user)

            user_auth.email = email
            user_auth.first_name = form.cleaned_data['first_name']
            user_auth.last_name = form.cleaned_data['last_name']
            user_auth.save()

            user = authenticate(request, username=user.username, password=password)
            login(request, user)
            return redirect('personal_area')
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})


@login_required
def personal_area(request):
    user = request.user

    context = {
        'user': user,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }

    return render(request, 'main/personal_area.html', context)


def save_field(request, field_name):
    if request.method == 'POST':
        value = request.POST.get(field_name)
        if value is not None:
            user = request.user
            user_auth = user.userauth
            setattr(user_auth, field_name, value)
            user_auth.save()
    return redirect('personal_area')


def save_phone(request):
    return save_field(request, 'phone')

def save_address(request):
    return save_field(request, 'address')

def save_city(request):
    return save_field(request, 'city')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('personal_area')
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')
    return render(request, 'main/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('main')
