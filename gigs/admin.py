from django.contrib import admin
from .models import *


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

class FileInline(admin.TabularInline):
    model = ResumeFile
    extra = 1

class ExprienceInline(admin.TabularInline):
    model = Experience
    extra = 1

class ResumeAdmin(admin.ModelAdmin):
    model = Resume
    inlines = [ EducationInline,ExprienceInline,FileInline ]


# Register your models here.
# admin.site.register(Job)
admin.site.register(Category)
admin.site.register(Service)
# admin.site.register(Resume,ResumeAdmin)
