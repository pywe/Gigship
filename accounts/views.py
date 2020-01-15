from django.shortcuts import render


# Create your views here.
# index page, showing homepage to users
def index(request):
    template_name = "accounts/index.html"
    args = {}
    return render(request,template_name,args)


# how it works page, showing how it works page to users
def how_it_works(request):
    template_name = "accounts/how-it-works.html"
    args = {}
    return render(request,template_name,args)


# registration page, showing registration page to users
def registration(request):
    template_name = "accounts/registration.html"
    args = {}
    return render(request,template_name,args)

# login page, showing login page to users
def login(request):
    template_name = "accounts/login.html"
    args = {}
    return render(request,template_name,args)

# forgot password page, showing forgot password page to users
def forgot(request):
    template_name = "accounts/forgot.html"
    args = {}
    return render(request,template_name,args)