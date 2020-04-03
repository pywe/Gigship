from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# from django_mysql.models import ListTextField


# Create your models here.

userTypes = (
    ('Admin','Admin'),
    ('Gigger','Gigger'),
    ('Shipper','Shipper')
    )

# First class model
class GiggerCategory(models.Model):
    name = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.name


class Credit(models.Model):
    username = models.CharField(max_length=200,blank=True,null=True)
    current_bal = models.FloatField(default=00.0,null=True)
    last_recharged = models.DateTimeField(blank=True,null=True,auto_now_add=True)
    exp_date = models.DateTimeField(null=True)
    last_transid = models.CharField(max_length=12,null=True,blank=True)
    cumulative_bal = models.FloatField(default=00.0,null=True)


    def __str__(self):
        return self.username

# First class model
class CustomUser(AbstractUser):
    # add additional fields in here
    phone = models.CharField(max_length=14,null=True)
    user_img = models.FileField(null=True,upload_to="static/profiles/")
    is_staff = models.BooleanField(default=False)
    user_type = models.CharField(max_length=20,choices=userTypes, null=True)
    credit = models.OneToOneField(Credit, null=True, blank=True,on_delete=models.SET_NULL)
    categories =models.ManyToManyField(GiggerCategory)



# Second class model
# Freelancer model:migrates into database as accounts_freelancer table
class Gigger(CustomUser):
    referral_token = models.CharField(max_length=30,null=True,blank=True)
    # categories =models.ManyToManyField(GiggerCategory)

    class Meta:
        verbose_name = "Gigger"




# Second class model
# Employer model:migrates into database as accounts_emploer table
class Shipper(CustomUser):
    referral_token = models.CharField(max_length=30,null=True,blank=True)

    class Meta:
        verbose_name = "Shipper"
        

class Message(models.Model):
    content = models.TextField(null=True,blank=True)
    date_created = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    date = models.DateField(null=True,blank=True,auto_now_add=True)
    time = models.TimeField(null=True,blank=True,auto_now_add=True)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank = True, on_delete = models.SET_NULL,related_name="to_user")
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank = True, on_delete = models.SET_NULL,related_name="from_user")
    sent = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    reply = models.ForeignKey("self",null=True, blank = True, on_delete = models.SET_NULL)


    def __str__(self):
        return "from {} to {}".format(str(self.from_user.username),str(self.to_user.username))


class MessageFile(models.Model):
    message = models.ForeignKey(Message,null=True, blank = True, on_delete = models.SET_NULL,related_name="files")
    name = models.CharField(max_length=50,null=True,blank=True)
    message_file = models.FileField(null=True,upload_to="static/messages/")
    date_created = models.DateTimeField(null=True,blank=True,auto_now_add=True)


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=12,unique=True)
    transaction_type = models.CharField(max_length=25,null=True)
    transaction_amount = models.FloatField(default=0.0)
    date_created = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    completed = models.BooleanField(default=False)
    r_switch = models.CharField(max_length=20,null=True)
    by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank = True, on_delete = models.SET_NULL,related_name="transactions")



    def __str__(self):
        return self.transaction_id
