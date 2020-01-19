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

# faq page, showing faq page to users
def faq(request):
    template_name = "accounts/faq.html"
    args = {}
    return render(request,template_name,args)

# create resume page, showing create resume page to users
def create_resume(request):
    template_name = "accounts/create-resume.html"
    args = {}
    return render(request,template_name,args)

# support page, showing support page to users
def support(request):
    template_name = "accounts/contact.html"
    args = {}
    return render(request,template_name,args)

# post job page, post job page to users
def post_job(request):
    template_name = "accounts/post-job.html"
    args = {}
    return render(request,template_name,args)

# dashboard page, dashboard page to users
def dashboard(request):
    template_name = "accounts/dashboard.html"
    args = {}
    return render(request,template_name,args)