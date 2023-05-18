from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission, Group
from django.db import models
from django.utils.translation import gettext as _

class CustomUserManager(BaseUserManager):
    """
    Custom user manager class extending BaseUserManager.

    This manager provides methods for creating user objects with specific attributes.

    Methods:
        create_user(email, password=None, **extra_fields):
            Creates and saves a regular user with the given email and password.
            
            Args:
                email (str): The email address of the user.
                password (str, optional): The password for the user. Defaults to None.
                **extra_fields: Additional fields and their values to be set for the user.
            
            Returns:
                User: The created user object.

            Raises:
                ValueError: If the email is not provided.

        create_superuser(email, password=None, **extra_fields):
            Creates and saves a superuser with the given email and password.
            
            Args:
                email (str): The email address of the superuser.
                password (str, optional): The password for the superuser. Defaults to None.
                **extra_fields: Additional fields and their values to be set for the superuser.
            
            Returns:
                User: The created superuser object.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    # Adding the related_name argument to the groups field
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='customuser_set')
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='customuser_permissions',  # Add related_name argument
        help_text=_('Specific permissions for this user.'),
        related_query_name='customuser',
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name
