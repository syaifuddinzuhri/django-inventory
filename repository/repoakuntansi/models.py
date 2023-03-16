import datetime
from enum import Enum
import os
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


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

    TIPE_CHOICES = (
        (SUPER_ADMIN, 'Super Admin'),
        (ADMIN, 'Admin'),
        (USER, 'User'),
    )

    nama = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=255, blank=True)
    nim = models.CharField(max_length=12, unique=True, null=True, blank=True)
    kode_prodi = models.CharField(max_length=100, null=True, blank=True)
    kelas = models.CharField(max_length=100, null=True, blank=True)
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
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    deskripsi = models.TextField(null=True)
    status = models.CharField(max_length=100)
    file = models.FileField(upload_to='file/', null=True)
    date = models.DateField(auto_now_add=True)
