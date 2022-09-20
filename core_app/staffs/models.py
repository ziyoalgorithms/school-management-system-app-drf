import os
import uuid
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from phone_field import PhoneField

from lesson.models import Subject


def image_file_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"

    return os.path.join('uploads/', 'students', filename)


class TeacherManager(BaseUserManager):
    def validateEmail(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Yaroqli email kiriting!")

    def create_superuser(self, email, password, **extra_fields):\

        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Admin uchun is_superuser=True bo'lishi kerak!")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Admin uchun is_staff=True bo'lishi kerak!")

        if email:
            email = self.normalize_email(email)
            self.validateEmail(email)
        else:
            raise ValueError("Admin akkaunt: Email manzilingizni kiriting!")

        return self.create_user(email, password, **extra_fields)

    def create_user(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)

        if email:
            email = self.normalize_email(email)
            self.validateEmail(email)
        else:
            raise ValueError("Foydalanuvchi akkaunti: Emailingizni kirting!")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save()

        return user


class Teacher(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    phone = PhoneField()
    subject = models.ForeignKey(
        Subject,
        related_name='subject_teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TeacherManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    father_name = models.CharField(max_length=32)
    image = models.ImageField(null=True, upload_to=image_file_path)
    birthday = models.DateField(blank=True, null=True)
    phone = PhoneField()
    gender = models.CharField(
        max_length=5,
        choices=(('ERKAK', 'Erkak'), ('AYOL', 'Ayol')),
        blank=True, null=True
    )
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
