from django.urls import path
from . import views
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logoutPage, name='logout'),
    path('login', views.loginPage, name='login'),
    path('login-submit', views.submitLogin, name='login-submit'),
    path('tugas', views.tugas, name='tugas'),
    path('profile', views.profile, name='profile'),
    path('jurnal', views.jurnal, name='jurnal'),
    path('pembimbing', views.pembimbing, name='pembimbing'),

    path('user', views.userList, name='user-list'),
    path('user/create', views.userCreate, name='user-create'),
    path('user/<id>/edit', views.userEdit, name='user-edit'),
    path('user/<id>/delete', views.userDelete, name='user-delete'),

    path('admins', views.adminList, name='admin-list'),
    path('admins/create', views.adminCreate, name='admin-create'),
    path('admins/<id>/edit', views.adminEdit, name='admin-edit'),
    path('admins/<id>/delete', views.adminDelete, name='admin-delete'),

    path('super-admin', views.superAdminList, name='super-admin-list'),
    path('super-admin/create', views.superAdminCreate, name='super-admin-create'),
    path('super-admin/<id>/edit', views.superAdminEdit, name='super-admin-edit'),
    path('super-admin/<id>/delete', views.superAdminDelete,
         name='super-admin-delete'),
]
