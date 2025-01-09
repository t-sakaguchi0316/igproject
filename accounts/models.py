#accounts/models
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    icon = models.ImageField(upload_to='icons/', null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)


