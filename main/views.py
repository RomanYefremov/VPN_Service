from urllib.parse import urljoin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserAuth, Site
from .forms import RegistrationForm
from .forms import SiteForm
import requests
from bs4 import BeautifulSoup



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
            return redirect('personal_area')
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
    user_sites = Site.objects.filter(user_auth=user.userauth)
    context = {
        'user': user,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'user_sites': user_sites,
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


def dashboard(request):
    if request.method == 'POST':
        site_id = request.POST.get('site_id')
        if site_id:
            site = get_object_or_404(Site, id=site_id)
            site.delete()
            return redirect('dashboard')

    user_sites = Site.objects.filter(user_auth=request.user.userauth)

    context = {
        'user_sites': user_sites,
    }

    return render(request, 'main/dashboard.html', context)


def proxy_site(request, site_name, path=''):
    user = request.user
    user_site = get_object_or_404(Site, user_auth__user=user, name=site_name)

    user_site.transitions_count += 1

    response = requests.get(path)

    external_content = response.content
    user_site.data_sent += len(request.body)
    user_site.data_received += len(response.content)

    user_site.save()

    internal_content = modify_links(path, external_content, site_name)
    return HttpResponse(internal_content, content_type=response.headers['content-type'])


def modify_links(new_base_url, external_content, site_name):
    soup = BeautifulSoup(external_content, 'html.parser')

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']

        if not href.startswith(('http://', 'https://')) or href.startswith(f'{new_base_url}'):
            modified_url = urljoin(new_base_url, href)
            a_tag['href'] = f"/{site_name}/{modified_url}"

    for tag in soup.find_all(['link', 'script', 'img'], src=True):
        src = tag['src']

        if not src.startswith(('http://', 'https://')) or src.startswith(f'{new_base_url}'):
            modified_url = urljoin(new_base_url, src)
            tag['src'] = f"/{site_name}/{modified_url}"

    for form_tag in soup.find_all('form', action=True):
        action = form_tag['action']

        if not action.startswith(('http://', 'https://')) or action.startswith(f'{new_base_url}'):
            modified_url = urljoin(new_base_url, action)
            form_tag['action'] = f"/{site_name}/{modified_url}"

    modified_content = str(soup)
    return modified_content
