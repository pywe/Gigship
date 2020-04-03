from django.db import models
from accounts.models import Shipper,GiggerCategory
from django.conf import settings

# Create your models here.

# First class model
class Skill(models.Model):
    name = models.CharField(max_length=50,null=True)


# Second class model
class Resume(models.Model):
    profession = models.CharField(max_length=50,null=True)
    years_experience = models.IntegerField(default=0)
    months_experience = models.IntegerField(default=0)
    skills = models.ManyToManyField(Skill)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank = True, on_delete = models.SET_NULL)


# Third class model
class Education(models.Model):
    resume = models.ForeignKey(Resume,null=True,on_delete=models.SET_NULL,related_name="education")
    school_name = models.CharField(max_length=100,null=True)
    qualification = models.CharField(max_length=100,null=True)
    period_from = models.DateField(null=True)
    period_to = models.DateField(null=True)


# Third class model
class Experience(models.Model):
    resume = models.ForeignKey(Resume,null=True,on_delete=models.SET_NULL,related_name="experiences")
    company_name = models.CharField(max_length=100,null=True)
    position = models.CharField(max_length=100,null=True)
    period_from = models.DateField(null=True)
    period_to = models.DateField(null=True)

# # Third class model
# class ResumeSkill(models.Model):
#     resume = models.ForeignKey(Resume,null=True,on_delete=models.SET_NULL,related_name="skills")
#     skills = models.ManyToManyField(Skill)

# Third class model
class ResumeFile(models.Model):
    resume = models.ForeignKey(Resume,null=True,on_delete=models.SET_NULL,related_name="files")
    resumefile = models.FileField(null=True,upload_to="static/resumes/")


# First class model
class Category(models.Model):
    name = models.CharField(max_length=50,null=True)

stata = (
    ('Active','Active'),
    ('Done','Done'),
    ('Cancelled','Cancelled')
)
# Second class model
class Job(models.Model):
    title = models.CharField(max_length=50,null=True)
    description = models.TextField(null=True)
    status = models.CharField(max_length=15,choices=stata,null=True,default="Active")
    category = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL)
    employer = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL)
    date_added = models.DateField(null=True,auto_now_add=True)


class Gig(models.Model):
    service = models.CharField(max_length=50,null=True)
    start_price = models.FloatField(default=0.0)
    categories = models.ManyToManyField(GiggerCategory)
    experience = models.IntegerField(default=0)
    service_detail = models.TextField(null=True)
    rating = models.FloatField(default=0.0)
    gigger = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL)
    

    class Meta:
        verbose_name = "Gig"

    def __str__(self):
        if self.gigger:
            return "{} by {} starting at GHC{}".format(self.service,self.gigger.username,self.start_price)
        else:
            return "{} starting at GHC{}".format(self.service,self.start_price)


# Third class model
class GigFile(models.Model):
    service = models.ForeignKey(Gig,null=True,on_delete=models.SET_NULL,related_name="files")
    servicefile = models.FileField(null=True,upload_to="static/services/")
    file_type = models.CharField(max_length=10,null=True,help_text="image,video,gif")

    class Meta:
        verbose_name = "Gig File"



class GigPlan(models.Model):
    gig = models.ForeignKey(Gig,null=True,on_delete=models.SET_NULL,related_name="plans")
    name = models.CharField(max_length=10,null=True,help_text="Basic,Standard,Premium")
    description = models.TextField(null=True)
    delivery_time = models.IntegerField(default=1,help_text="Number of days")
    revision = models.IntegerField(default=1,help_text="How many times will you review?")
    price = models.FloatField(default=0.0)
    


# add extra features to gig
class Extra(models.Model):
    gig = models.ForeignKey(Gig,null=True,on_delete=models.SET_NULL,related_name="extras")
    name = models.CharField(max_length=50,null=True)
    description = models.TextField(null=True)
    additional_time = models.IntegerField(default=0,help_text="will this feature increase delivery time?")
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    order_no = models.CharField(max_length=30,null=True)
    gigs = models.ManyToManyField(Gig,related_name="gigs")
    total_price = models.FloatField(default=0.0)
    VAT = models.FloatField(default=0.0)
    commission = models.FloatField(default=0.0)
    order_price = models.FloatField(default=0.0)
    date_created = models.DateTimeField(null=True,auto_now_add=True)
    status = models.CharField(max_length=20,null=True)
    delivery_time = models.IntegerField(default=0)
    date_to_complete = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(null=True)
    order_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL)
    extras = models.ManyToManyField(Extra)
    plan = models.ForeignKey(GigPlan,null=True,on_delete=models.SET_NULL)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.order_no


class Customization(models.Model):
    order = models.ForeignKey(Order,null=True,on_delete=models.SET_NULL,related_name="customizations")
    total_price = models.FloatField(default=0.0)
    VAT = models.FloatField(default=0.0)
    commission = models.FloatField(default=0.0)


class Rating(models.Model):
    gig = models.ForeignKey(Gig,null=True,on_delete=models.SET_NULL,related_name="ratings")
    rating = models.FloatField(default=1)
    review = models.TextField(null=True)
    rated_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL)


modes = (
    ('created','created'),
    ('quoted','quoted'),
    ('transit','transit'),
    ('completed','completed')
)

class Request(models.Model):
    request = models.CharField(max_length=50,null=True)
    detail = models.TextField(null=True,help_text="This should say what the client wants")
    category = models.ForeignKey(GiggerCategory,null=True,on_delete=models.SET_NULL,help_text="To what specialty do we classify this request")
    updated = models.BooleanField(default=False)
    time_updated = models.DateTimeField(null=True,blank=True)
    completed = models.BooleanField(default=False)
    time_completed = models.DateTimeField(null=True,blank=True)
    mode = models.CharField(max_length=20,null=True,choices=modes,default='created')
    date_time_created = models.DateTimeField(null=True, auto_now_add=True)
    date_created = models.DateField(null=True, auto_now_add=True)
    time_created = models.TimeField(null=True, auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL,help_text="Who actually created the request?")
    request_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL,related_name="request_by",help_text="The client who created this request")


    def __str__(self):
        if self.category:
            return self.category.name
        else:
            return self.detail


# This model is for quotes that will be created
# Third class model because it depends directly on request model
class Quote(models.Model):
    request = models.ForeignKey(Request,null=True,on_delete=models.SET_NULL,related_name="quotes")
    date_time_submitted = models.DateTimeField(null=True, auto_now_add=True)
    date_submitted = models.DateField(null=True, auto_now_add=True)
    time_submitted = models.TimeField(null=True, auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL,help_text="Who created the quote?")
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL,related_name="submitted_by",help_text="Who was this quote created for?")
    updated = models.BooleanField(default=False)
    time_updated = models.DateTimeField(null=True,blank=True)
    accepted = models.BooleanField(default=False)
    time_accepted = models.DateTimeField(null=True,blank=True)


    def __str__(self):
        return "Quote submitted for {} by {}".format(self.request,self.submitted_by.username)

