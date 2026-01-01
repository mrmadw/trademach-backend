from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    """
    Custom manager for NewUser.
    Handles creation of regular users and superusers.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a regular user.
        Accepts email, password, and any other optional fields.
        """
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)       

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser.
        Accepts email and password. Other fields come via extra_fields.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password=password, **extra_fields)


class NewUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.
    """

    email = models.EmailField(_("email address"), unique=True)

    # Optional, public profile
    username = models.CharField(max_length=150, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_verified = models.BooleanField(default=False)

    # Admin + access control
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  
   # REQUIRED_FIELDS = ["username", "first_name"]   Uncomment when you want to create superuser. Make sure to comment out the one above!

    def __str__(self):
        return self.email
