from django.shortcuts import render,redirect,HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout


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
    if request.method == "GET":
        template_name = "accounts/registration.html"
        args = {}
        return render(request,template_name,args)
    else:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        account_type = request.POST['account_type']
        if account_type == "freelancer":
            user = Freelancer()
        else:
            user = Employer()
        user.username = username
        user.email = email
        user.set_password(password)
        try:
            user.save()
        except Exception as e:
            messages.error(request,str(e))
            return redirect("/accounts/registration/")
        msg = """Hello {}, we are excited to have you on board. 
        Here is your link ### to verify your email and officially be accepted on the platform as a/an {}""".format(username,account_type)
        send_mail(
        'Welcome To Gigship',
        msg,
        'pythonwithelli@gmail.com',
        [email],
        fail_silently=False,
        )
        messages.success(request,"Account created. Please verify your mail")
        return redirect("/accounts/registration/")


# login page, showing login page to users
def mylogin(request):
    if request.method == "GET":
        template_name = "accounts/login.html"
        args = {}
        return render(request,template_name,args)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request,"login successful")
        return redirect("/")
    else:
        messages.error(request,"Failed. Please check your credentials")
        return redirect("/accounts/login/")


def mylogout(request):
    logout(request)
    messages.success(request,"Thanks for spending time with us")
    return redirect('/')

    
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

# support page, showing support page to users
def support(request):
    template_name = "accounts/contact.html"
    args = {}
    return render(request,template_name,args)

# dashboard page, dashboard page to users
def dashboard(request):
    template_name = "accounts/dashboard.html"
    args = {}
    return render(request,template_name,args)


# myjobs page, myjobs page to users
def myjobs(request):
    template_name = "accounts/myjobs.html"
    args = {}
    return render(request,template_name,args)


@csrf_exempt
def create_freelancer(request):
    json_data = json.loads(str(request.body, encoding='utf-8'))
    username = json_data['username']
    email = json_data['email']
    password = json_data['password']
    user = Freelancer()
    user.username = username
    user.set_password(password)
    user.email = email
    user.save()
    # send mail to user here
    data = {
    'success':True,
    'message':"Freelancer created"}
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')


@csrf_exempt
def create_employer(request):
    json_data = json.loads(str(request.body, encoding='utf-8'))
    username = json_data['username']
    email = json_data['email']
    password = json_data['password']
    user = Employer()
    user.username = username
    user.set_password(password)
    user.email = email
    user.save()
    # send mail to user here
    data = {
    'success':True,
    'message':"Employer created"}
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')

