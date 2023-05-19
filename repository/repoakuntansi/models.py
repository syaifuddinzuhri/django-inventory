import datetime
from enum import Enum
import os
import random
import string
import time
from uuid import uuid4
import uuid
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from django.utils.deconstruct import deconstructible


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):

    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    USER = "USER"
    PEMBIMBING = "PEMBIMBING"

    TIPE_CHOICES = (
        (SUPER_ADMIN, 'Super Admin'),
        (ADMIN, 'Admin'),
        (USER, 'User'),
        (PEMBIMBING, 'Pembimbing'),
    )

    nama = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=255, blank=True)
    nim = models.CharField(max_length=12, unique=True, null=True, blank=True)
    kode_prodi = models.CharField(max_length=100, null=True, blank=True)
    kelas = models.CharField(max_length=100, null=True, blank=True)
    nip = models.CharField(max_length=100, null=True, blank=True)
    tipe = models.CharField(
        max_length=255, choices=TIPE_CHOICES, default=USER, blank=True)

    # USERNAME_FIELD = 'nim'
    # REQUIRED_FIELDS = ["username"]

    # def __str__(self):
    #     return self.username


# def filepath(request, filename):
#     old_filename = filename
#     timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
#     filename = "%s%s" % (timeNow, old_filename)
#     return os.path.join('uploads/', filename)


class Jurnal(models.Model):
    def upload_pdf_validator(upload_pdf_obj):
        ext = os.path.splitext(upload_pdf_obj.name)[
            1]
        valid_extension = ['.pdf', '.docx', '.doc']
        if not ext in valid_extension:
            raise ValidationError(
                u'Unsupported file extension, .pdf/.doc/.docx only.')

    user = models.ForeignKey("User", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    deskripsi = models.TextField(null=True)
    status = models.CharField(max_length=100)
    file = models.FileField(
        upload_to='file/', validators=[upload_pdf_validator], null=True)
    date = models.DateField(auto_now_add=True)


class TugasAkhir(models.Model):

    def upload_pdf_validator(upload_pdf_obj):
        ext = os.path.splitext(upload_pdf_obj.name)[
            1]
        valid_extension = ['.pdf', '.docx', '.doc']
        if not ext in valid_extension:
            raise ValidationError(
                u'Unsupported file extension, .pdf/.doc/.docx only.')

    user = models.ForeignKey(
        User, related_name='related_user_manual_roats', verbose_name="User", on_delete=models.CASCADE)
    pembimbing = models.ForeignKey(
        User, related_name='related_pembimbing_manual_roats', verbose_name="Pembimbing", on_delete=models.CASCADE)
    judul = models.CharField(max_length=255, null=True)
    deskripsi = models.TextField(null=True)
    catatan = models.TextField(null=True)
    komentar = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, null=True)
    file = models.FileField(upload_to='file/',
                            validators=[upload_pdf_validator], null=True)
    date = models.DateField(auto_now_add=True)
