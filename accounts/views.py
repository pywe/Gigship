from django.shortcuts import render, redirect, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from gigs.models import Gig
from datetime import datetime,date, timedelta



# Create your views here.
# index page, showing homepage to users
def index(request):
    if request.user.is_authenticated:
        links = {'Gigger': 'accounts/dashboard.html',
                 'Shipper': 'accounts/index.html', 'Admin': 'accounts/index.html'}
        try:
            template_name = links[request.user.user_type]
        except:
            template_name = "accounts/index.html"
        categories = GiggerCategory.objects.all()
        args = {'categories': categories}
        return render(request, template_name, args)
    else:
        return redirect("/accounts/login/")

# myjobs page, myjobs page to users


def mygigs(request):
    if request.user.is_authenticated:
        links = {'Gigger': 'accounts/mygigs.html',
                 'Shipper': 'accounts/mygigs.html', 
                 'Admin': 'accounts/mygigs.html'}
        try:
            template_name = "accounts/mygigs.html"
        except:
            template_name = "accounts/mygigs.html"
        services = Gig.objects.filter(gigger=request.user)
        args = {'services': services}
        return render(request, template_name, args)
    else:
        return redirect("/accounts/login/")

# how it works page, showing how it works page to users


def myorders(request):
    template_name = "accounts/myorders.html"
    args = {}
    return render(request, template_name, args)

# settings page, showing settings page to users


def mysettings(request):
    template_name = "accounts/settings.html"
    args = {}
    return render(request, template_name, args)

# how it works page, showing how it works page to users


def how_it_works(request):
    template_name = "accounts/how-it-works.html"
    args = {}
    return render(request, template_name, args)

# services page, showing services page to users


def services(request):
    template_name = "accounts/services.html"
    args = {}
    return render(request, template_name, args)


# registration page, showing registration page to users
def registration(request):
    if request.method == "GET":
        template_name = "accounts/registration.html"
        categories = GiggerCategory.objects.all()
        args = {'categories': categories}
        return render(request, template_name, args)
    else:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # account_type = request.POST['account_type']
        # if account_type == "Gigger":
        #     user = Gigger()
        #     user.user_type = 'Gigger'
        user = CustomUser()
        category1 = request.POST['category1']
        category2 = request.POST['category2']
        try:
            real_1 = GiggerCategory.objects.get(name=category1)
        except:
            pass
        else:
            user.categories.add(real_1)
        try:
            real_2 = GiggerCategory.objects.get(name=category2)
        except:
            pass
        else:
            user.categories.add(real_2)

        # else:
        #     user = Shipper()
        #     user.user_type = 'Shipper'
        user.username = username
        user.email = email
        user.set_password(password)
        try:
            user.save()
        except Exception as e:
            messages.error(request, str(e))
            return redirect("/accounts/registration/")
        # create credit for user
        today = date.today()
        exp_date = today + timedelta(30*6)
        credit = Credit(username=username,current_bal=0.0,exp_date=exp_date)
        credit.save()
        user.credit = credit
        user.save()
        msg = """Hello {}, we are excited to have you on board.
        Here is your link ### to verify your email and officially be accepted on the platform as a/an {}""".format(username, account_type)
        send_mail(
            'Welcome To Gigship',
            msg,
            'pythonwithelli@gmail.com',
            [email],
            fail_silently=False,
        )
        messages.success(request, "Account created. Please verify your mail")
        return redirect("/accounts/registration/")


# login page, showing login page to users
def mylogin(request):
    if request.method == "GET":
        template_name = "accounts/login.html"
        categories = GiggerCategory.objects.all()
        args = {'categories': categories}
        return render(request, template_name, args)
    links = {'Gigger': '/accounts/dashboard/', 'Shipper': '/', 'Admin': '/'}
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, "login successful")
        link = links[user.user_type]
        return redirect(link)
    else:
        messages.error(request, "Failed. Please check your credentials")
        return redirect("/accounts/login/")


def mylogout(request):
    logout(request)
    messages.success(request, "Thanks for spending time with us")
    return redirect('/')


# forgot password page, showing forgot password page to users
def forgot(request):
    template_name = "accounts/forgot.html"
    args = {}
    return render(request, template_name, args)

def chat(request):
    template_name = "accounts/chat.html"
    args = {}
    return render(request, template_name, args)

# faq page, showing faq page to users


def faq(request):
    template_name = "accounts/faq.html"
    args = {}
    return render(request, template_name, args)

# support page, showing support page to users


def support(request):
    template_name = "accounts/contact.html"
    args = {}
    return render(request, template_name, args)

# dashboard page, dashboard page to users


def dashboard(request):
    template_name = "accounts/dashboard.html"
    args = {}
    return render(request, template_name, args)

# profil page, profil page to users


def add_services(request):
    if request.user.is_authenticated:
        template_name = "accounts/profil.html"
        categories = GiggerCategory.objects.all()
        args = {'categories': categories}
        return render(request, template_name, args)
    else:
        return redirect("/accounts/login/")


import requests as r
def payment(request):
    if request.method == "GET":
        # status = request.GET['status']
        transid = request.GET['transaction_id']
        t_id = str(transid)
        order = Transaction.objects.get(transaction_id=t_id)
        # print(transid)
        #reason = request.GET['reason']
        # code = request.GET['code']
        url = "https://test.theteller.net/v1.1/users/transactions/{}/status/".format(transid)
        header = {'Merchant-Id':"TTM-00000278"}
        response = r.get(url,headers=header)
        json_data = json.loads(response.text)
        print(response.text)
        """Check if transaction was succesful first"""
        if json_data['status'] == "approved":
            if order.completed:
                messages.error(request, "Order Already Confirmed")
                return redirect('/accounts/top-up/')
            else:
                order.complete = True
                order.save()
                user = order.by
                if user.credit:
                    credit = user.credit
                    credit.current_bal += float(json_data['amount'])
                    credit.last_transid = t_id
                    credit.last_recharge = datetime.now()
                    credit.save()
                messages.success(request, "Transaction successful")
                return redirect('/accounts/top-up/')
        # TODO: notify user
        # amount = json_data['amount']
        # source = json_data['subscriber_number']
        # network = json_data['r_switch']
        # status = json_data['status']
        #reason = json_data['reason']
        #transaction = Transaction()
        # transaction.amount = amount
        # transaction.transid = transid
        # transaction.source = source
        # transaction.network = network
        # transaction.user = request.user
        #transaction.response = reason
        # if status == "approved":
        #     transaction.status = True
        #     user_credit = Credit.objects.get(user=request.user)
        #     user_credit.last_transid = transid
        #     user_credit.current_bal += amount
        # user_credit.save()
        # transaction.save()
        messages.error(request, "{}".format(json_data['reason']))
        return redirect('/accounts/top-up/')



@csrf_exempt
def create_gigger(request):
    json_data = json.loads(str(request.body, encoding='utf-8'))
    username = json_data['username']
    email = json_data['email']
    password = json_data['password']
    user = Gigger()
    user.username = username
    user.set_password(password)
    user.email = email
    user.save()
    # send mail to user here
    data = {
        'success': True,
        'message': "Gigger created"}
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')


@csrf_exempt
def create_shipper(request):
    json_data = json.loads(str(request.body, encoding='utf-8'))
    username = json_data['username']
    email = json_data['email']
    password = json_data['password']
    user = Shipper()
    user.username = username
    user.set_password(password)
    user.email = email
    user.save()
    # send mail to user here
    data = {
        'success': True,
        'message': "Shipper created"}
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')


def gen_order_no(number):
    if number > 0:
        no = str(number+1)
    else:
        no = str(1)
    return no.rjust(12, '0')


@csrf_exempt
def create_transaction(request):
    json_data = json.loads(str(request.body, encoding='utf-8'))
    data = {}
    username = json_data['user']
    amount = json_data['amount']
    try:
        user = CustomUser.objects.get(username=username)
    except:
        data['success']=False
        data['message']="User does not exists"
    else:
        all_trans = len(Transaction.objects.all())
        transaction = Transaction()
        transaction.transaction_id = gen_order_no(all_trans)
        transaction.transaction_type = "Top-up"
        transaction.transaction_amount = float(amount)
        transaction.save()
        transaction.by = user
        transaction.save()
        obj={
            "transid":transaction.transaction_id,
            "amount":transaction.transaction_amount,
        }
        data['success']=True
        data['message']="Transaction successful"
        data['data']=obj
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')



def buy_credit(request):
    if request.user.is_authenticated:
        template_name = "accounts/buy-credit.html"
        args = {}
        args['zanzama']="ODEwN2ZiZjA5MWRhZGVhYWU2YWFmOWJhMGFkMjhlNjQ="
        return render(request,template_name,args)
    else:
        return redirect('/accounts/login/')





