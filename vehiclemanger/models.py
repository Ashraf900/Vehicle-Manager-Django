from enum import unique
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from .validators import isalphanumvalidator




class UserManager(BaseUserManager):
    def create_user(self, email, name,city, password=None, password2=None):
        """
        Creates and saves a User with the given email,name,tc
         and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name = name,
            city = city,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name,city, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name =name,
            city = city,
        )
        user.is_admin = True
        user.is_superuser=True
        user.save(using=self._db)
        return user




class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    city = models.CharField(max_length = 200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default = False)
    created_a = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','city']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class VehiclesTab(models.Model):
    choice_type = (
        ('Two Wheeler','Two Wheeler'),
        ('Two Wheeler','Three Wheeler'),
        ('Two Wheeler' ,'Four Wheeler')
        )
    vehicle_number = models.CharField(max_length = 50, validators=[isalphanumvalidator], unique=True)
    vehicle_type = models.CharField(max_length= 100, choices= choice_type)
    vehicle_model = models.CharField(max_length = 100)
    vehicle_desc = models.CharField(max_length = 200)
    
    def __str__ (self):
        return self.vehicle_number