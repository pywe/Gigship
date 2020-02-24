from django.db import models
from accounts.models import Employer
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


class Service(models.Model):
    service = models.CharField(max_length=50,null=True)
    start_price = models.FloatField(default=0.0)
    category = models.CharField(max_length=50,null=True)
    experience = models.IntegerField(default=0)
    service_detail = models.TextField(null=True)
    rating = models.FloatField(default=0.0)
    gig = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.SET_NULL)

    def __str__(self):
        if self.gig:
            return "{} by {} starting at GHC{}".format(self.service,self.gig.username,self.start_price)
        else:
            return "{} starting at GHC{}".format(self.service,self.start_price)


# Third class model
class ServiceFile(models.Model):
    service = models.ForeignKey(Service,null=True,on_delete=models.SET_NULL,related_name="files")
    servicefile = models.FileField(null=True,upload_to="static/services/")