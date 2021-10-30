from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .managers import CustomUserManager


class Country(models.Model):
    name = models.CharField(max_length=250, unique=True, verbose_name='Country', blank=True, null=True)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, unique=True, on_delete=models.CASCADE, verbose_name='Country', blank=True, null=True)
    name = models.CharField(max_length=250, unique=True, verbose_name='City', blank=True, null=True)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(max_length=250, unique=True, verbose_name='Name', blank=True, null=True)

    class Meta:
        verbose_name = 'Gender'
        verbose_name_plural = 'Genders'

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_index=True, unique=True, blank=True, null=True, verbose_name='Email')
    password = models.CharField(max_length=128, blank=True, null=True, verbose_name='Password')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_simple_user = models.BooleanField(verbose_name='User')
    is_professor = models.BooleanField(verbose_name='Admin')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Date of Registration')
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    is_superuser = models.BooleanField(default=False, verbose_name='Super admin')

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User',
                                related_name='user_profile')
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Name')
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Lastname')
    gender = models.ForeignKey(Gender, verbose_name='Gender', on_delete=models.CASCADE, null=True, blank=True)
    age = models.PositiveIntegerField(verbose_name='Age', null=True, blank=True)
    phone = models.CharField(max_length=100, blank=True, null=True, verbose_name='Phone')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Country', null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='City', null=True, blank=True)

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profile'

    def __str__(self):
        return '{}'.format(self.user)