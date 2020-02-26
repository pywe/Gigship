from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# from django_mysql.models import ListTextField


# Create your models here.

# First class model
class CustomUser(AbstractUser):
    # add additional fields in here
    phone = models.CharField(max_length=14,null=True)
    user_img = models.FileField(null=True,upload_to="static/profiles/")
    is_staff = models.BooleanField(default=False)


# Second class model
# Freelancer model:migrates into database as accounts_freelancer table
class Gigger(CustomUser):
    referral_token = models.CharField(max_length=30,null=True,blank=True)

    class Meta:
        verbose_name = "Gigger"


# Second class model
# Employer model:migrates into database as accounts_emploer table
class Buyer(CustomUser):
    referral_token = models.CharField(max_length=30,null=True,blank=True)

    class Meta:
        verbose_name = "Buyer"

