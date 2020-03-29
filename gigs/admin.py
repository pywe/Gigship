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

class ServiceFileInline(admin.TabularInline):
    model = ServiceFile
    extra = 1

class ResumeAdmin(admin.ModelAdmin):
    model = Resume
    inlines = [ EducationInline,ExprienceInline,FileInline ]


class ServiceAdmin(admin.ModelAdmin):
    model = Service
    inlines = [ ServiceFileInline,]


# Register your models here.
# admin.site.register(Job)
# admin.site.register(Category)
admin.site.register(ServiceFile)
admin.site.register(Service,ServiceAdmin)
# admin.site.register(Resume,ResumeAdmin)
