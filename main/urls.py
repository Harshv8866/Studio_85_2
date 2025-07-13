from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),

    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),

    path('upload-media/', views.upload_media, name='upload_media'),

    # in urls.py
path('service-detail/<int:service_id>/', views.service_detail, name='service_detail'),

path('rename-service/<int:service_id>/', views.rename_service, name='rename_service'),
path('delete-media/<int:media_id>/', views.delete_media, name='delete_media'),
path('delete-media-ajax/<int:media_id>/', views.delete_media_ajax, name='delete_media_ajax'),

path('admin/delete-inquiry/<int:msg_id>/', views.delete_inquiry, name='delete_inquiry'),





]
