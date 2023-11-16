from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import UserAuth

admin.site.register(UserAuth)
