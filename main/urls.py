from django.urls import path
from . import views
from .views import proxy_site, dashboard

urlpatterns = [
    path('', views.personal_area, name='main'),
    path('register/', views.register, name='register'),
    path('personal_area/', views.personal_area, name='personal_area'),
    path('save_phone/', views.save_phone, name='save_phone'),
    path('save_city/', views.save_city, name='save_city'),
    path('save_address/', views.save_address, name='save_address'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create-site/', views.create_site, name='create_site'),
    path('dashboard/', dashboard, name='dashboard'),
    path('<str:site_name>/<path:path>', proxy_site, name='proxy_site'),
]
