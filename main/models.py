from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserAuth(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=True)  # New field for first name
    last_name = models.CharField(max_length=50, null=True)  # New field for last name
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)  # Added phone field
    city = models.CharField(max_length=100)  # New field for city
    address = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else str(self.user.username)


class Site(models.Model):
    user_auth = models.ForeignKey(UserAuth, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.URLField()
    transitions_count = models.PositiveIntegerField(default=0)
    data_sent = models.PositiveIntegerField(default=0)
    data_received = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class VpnServer(models.Model):
    pass


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserAuth.objects.get_or_create(user=user, name=user.username, email=user.email)
        return user
