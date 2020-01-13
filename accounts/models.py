from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django_mysql.models import ListTextField


# Create your models here.
class CustomUser(AbstractUser):
    # add additional fields in here
    is_staff = models.BooleanField(default=False)


# Freelancer model:migrates into database as accounts_freelancer table
class Freelancer(CustomUser):
    referral_token = models.CharField(max_length=30,null=True,blank=True)

    class Meta:
        verbose_name = "Freelancer"


# Employer model:migrates into database as accounts_emploer table
class Employer(CustomUser):
    referral_token = models.CharField(max_length=30,null=True,blank=True)

    class Meta:
        verbose_name = "Employer"

