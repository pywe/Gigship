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

class GigFileInline(admin.TabularInline):
    model = GigFile
    extra = 1

class ResumeAdmin(admin.ModelAdmin):
    model = Resume
    inlines = [ EducationInline,ExprienceInline,FileInline ]


class GigAdmin(admin.ModelAdmin):
    # list_display = ['id',]
    model = Gig
    inlines = [ GigFileInline,]


# Register your models here.
# admin.site.register(Job)
# admin.site.register(Category)
admin.site.register(Order)
admin.site.register(GigFile)
admin.site.register(Gig,GigAdmin)
# admin.site.register(Resume,ResumeAdmin)
