from urllib.parse import urlparse, urljoin

from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserAuth, Site
from .forms import RegistrationForm
from .forms import SiteForm
import requests
from bs4 import BeautifulSoup
from django.db.models import Avg
import json
import datetime


def main(request):
    return render(request, 'main/main.html')


def create_site(request):
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            user_auth = UserAuth.objects.get(user=request.user)
            site = form.save(commit=False)
            site.user_auth = user_auth
            site.save()
            return redirect('personal_area')  # Adjust the URL name as needed
    else:
        form = SiteForm()

    return render(request, 'main/create_site.html', {'form': form})


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
    user_auth = UserAuth.objects.get(user=request.user)
    user_sites = Site.objects.filter(user_auth=user_auth)
    # user_site = get_object_or_404(Site, name=site_name)

    context = {
        'user': user,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'user_sites': user_sites,
        # 'site': user_site
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


def proxy_site(request, site_name, path=''):
    user_site = get_object_or_404(Site, name=site_name)

    # Check if the requested path is external (starts with 'http://' or 'https://')
    if path.startswith(('http://', 'https://')):
        external_url = path
    else:
        # Construct the URL of the external site
        external_url = f"{user_site.url}/{path}"

    # Fetch the content of the external site
    response = requests.get(external_url)
    external_content = response.content

    # Modify the links in the content to use internal routing
    internal_content = modify_links(path, external_content, site_name)
    return HttpResponse(internal_content, content_type=response.headers['content-type'])


def modify_links(new_base_url, external_content, site_name):
    soup = BeautifulSoup(external_content, 'html.parser')

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']

        if not href.startswith((f'http://', 'https://')):
            modified_url = urljoin(new_base_url, href)
            a_tag['href'] = f"/{site_name}/{modified_url}"

    for tag in soup.find_all(['link', 'script', 'img'], src=True):
        src = tag['src']

        if not src.startswith(('http://', 'https://')):
            modified_url = urljoin(new_base_url, src)
            tag['src'] = f"/{site_name}/{modified_url}"

    for form_tag in soup.find_all('form', action=True):
        action = form_tag['action']

        if not action.startswith(('http://', 'https://')):
            modified_url = urljoin(new_base_url, action)
            form_tag['action'] = f"/{site_name}/{modified_url}"

    # Convert the modified content back to a string
    modified_content = str(soup)
    return modified_content

