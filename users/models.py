from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    
    """
    Custom User model that extends the default Django User model.
    """
    
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True, null=True)
    actions_count = models.PositiveIntegerField(default=0)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    def __str__(self):
        """
        Returns a string representation of the user.
        """
        return self.username
    
    def increment_actions_count(self):
        """
        Increments the user's actions count by 1 and saves the user instance.
        """
        self.actions_count += 1
        self.save()
    
    def cls_last_activity(self):
        """
        Clears the last activity field of the user and saves the user instance.
        """
        self.last_activity = ''
        self.save()
