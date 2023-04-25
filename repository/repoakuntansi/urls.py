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
    path('profile', views.profile, name='profile'),

    path('user', views.userList, name='user-list'),
    path('user/create', views.userCreate, name='user-create'),
    path('user/<id>/edit', views.userEdit, name='user-edit'),
    path('user/<id>/delete', views.userDelete, name='user-delete'),

    path('pembimbing', views.pembimbingList, name='pembimbing-list'),
    path('pembimbing/create', views.pembimbingCreate, name='pembimbing-create'),
    path('pembimbing/<id>/edit', views.pembimbingEdit, name='pembimbing-edit'),
    path('pembimbing/<id>/delete', views.pembimbingDelete,
         name='pembimbing-delete'),

    path('admins', views.adminList, name='admin-list'),
    path('admins/create', views.adminCreate, name='admin-create'),
    path('admins/<id>/edit', views.adminEdit, name='admin-edit'),
    path('admins/<id>/delete', views.adminDelete, name='admin-delete'),

    path('super-admin', views.superAdminList, name='super-admin-list'),
    path('super-admin/create', views.superAdminCreate, name='super-admin-create'),
    path('super-admin/<id>/edit', views.superAdminEdit, name='super-admin-edit'),
    path('super-admin/<id>/delete', views.superAdminDelete,
         name='super-admin-delete'),

    path('tugas-akhir', views.tugasAkhirList, name='tugas-akhir-list'),
    path('tugas-akhir/create', views.tugasAkhirCreate, name='tugas-akhir-create'),
    path('tugas-akhir/<id>/edit', views.tugasAkhirEdit, name='tugas-akhir-edit'),
    path('tugas-akhir/<id>/delete', views.tugasAkhirDelete,
         name='tugas-akhir-delete'),

    path('jurnal/export', views.exportJurnal, name='jurnal-export'),
    path('jurnal', views.jurnalList, name='jurnal-list'),
    path('jurnal/create', views.jurnalCreate, name='jurnal-create'),
    path('jurnal/<id>/edit', views.jurnalEdit, name='jurnal-edit'),
    path('jurnal/<id>/delete', views.jurnalDelete,
         name='jurnal-delete'),
]
