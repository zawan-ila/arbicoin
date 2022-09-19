from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class MyUser(AbstractUser):
    pubkey = models.CharField(max_length=96)
    privkey = models.CharField(max_length=48)
