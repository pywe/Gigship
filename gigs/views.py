from django.shortcuts import render,redirect,HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from accounts.models import CustomUser
from .models import *
from django.contrib import messages
from datetime import datetime,date, timedelta



def order(request,id):
    template_name = "accounts/order.html"
    # get all necessary order details to displayed to the user
    args = {}
    gig = Gig.objects.get(id=int(id))
    args['gig']=gig
    args['zanzama']="ODEwN2ZiZjA5MWRhZGVhYWU2YWFmOWJhMGFkMjhlNjQ="
    return render(request,template_name,args)


# Create your views here.
# This view is used to create new resume through api call
@csrf_exempt
def create_resume(request):
    json_data = json.loads(str(request.body, encoding='utf-8'))
    username = json_data['username']
    # Get this freelancer with the username
    user = CustomUser.objects.get(username=username)
    profession = json_data['profession']
    years_exp = json_data['years_experiences']
    months_exp = json_data['months_experiences']
    # expects a list of skills
    skills = json_data['skills']
    # expects a list of education objects
    educations = json_data['educations']
    experiences = json_data['experiences']
    # after successfully getting everything, let's create a resume
    resume = Resume()
    resume.profession = profession
    resume.years_experience = int(years_exp)
    resume.months_experience = int(months_exp)
    resume.user = user
    resume.save()
    for exp in experiences:
        experience = Experience()
        experience.period_from = exp['from']
        experience.period_to = exp['to']
        experience.company_name = exp['company']
        experience.position = exp['position']
        experience.resume = resume
        experience.save()
    for educ in educations:
        education = Education()
        education.period_from = educ['from']
        education.period_to = educ['to']
        education.school_name = educ['school']
        education.qualification = educ['qualification']
        education.resume = resume
        education.save()
    # get skills
    for i in skills:
        try:
            skill = Skill.objects.get(name=i)
        except:
            pass
        else:
            resume.skills.add(skill)
            resume.save()
    # if everything goes well
    data = {
    'success':True,
    'message':"resume created"}
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')


@csrf_exempt
def create_job(request):
    json_data = json.loads(str(request.body, encoding='utf-8'))
    username = json_data['username']
    user = CustomUser.objects.get(username=username)
    title = json_data['title']
    description = json_data['description']
    category = json_data['category']
    cat = Category.objects.get(name=category)
    job = Job()
    job.title = title
    job.description = description
    job.category = cat
    job.employer = user
    job.save()
    data = {
    'success':True,
    'message':"Job created"}
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')


@csrf_exempt
def create_services(request):
    json_data = json.loads(str(request.body, encoding='utf-8'))
    # print(json_data)
    objs = []
    services = json_data['services']
    username = json_data['username']
    try:
        user = CustomUser.objects.get(username=username)
    except:
        user = None
    for s in services:
        service = s['service']
        start_price = int(s['start_price'])
        category = s['category']
        experience = s['experience']
        service_detail = s['service_detail']
        servicefile = s['file']
        myservice = Gig()
        myservice.service = service
        myservice.start_price = start_price
        myservice.save()
        try:
            real_cat = GiggerCategory.objects.get(name=category)
        except:
            pass
        else:
            myservice.categories.add(real_cat)
        myservice.experience = experience
        myservice.service_detail = service_detail
        myservice.save()
        if user:
            myservice.gigger = user
        myservice.save()
        # Let's create a basic plan for this gig
        plan = GigPlan()
        plan.name = "Basic"
        plan.delivery_time = 7
        plan.revision = 1
        plan.price = start_price
        plan.description = "Covers basic requirements for this gig"
        plan.save()
        plan.gig = myservice
        plan.save()
         # Let's create a standard plan for this gig
        plan = GigPlan()
        plan.name = "Standard"
        plan.delivery_time = 4
        plan.revision = 3
        plan.price = start_price + (start_price/4)
        plan.description = "Reduce delivery time and more revisions"
        plan.save()
        plan.gig = myservice
        plan.save()
         # Let's create a premium plan for this gig
        plan = GigPlan()
        plan.name = "Premium"
        plan.delivery_time = 2
        plan.revision = 5
        plan.price = start_price + (start_price/2)
        plan.description = "The best value for your money"
        plan.save()
        plan.gig = myservice
        plan.save()

        obj = {}
        obj['fileId']=servicefile
        obj['serviceId']= myservice.id
        objs.append(obj)
    data = {
    'success':True,
    'message':"Services created",
    "services":objs}
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')


def file_check(name):

    images = ['jpg','jpeg','png','svg','webp']
    name_list = name.split(".")
    if name_list[-1] in images:
        return "image"
    else:
        return "video"


@csrf_exempt
def add_service_files(request,id):
    try:
        files = request.FILES
    except Exception as e:
        print(e)
    try:
        service = Gig.objects.get(id=int(id))
    except Exception as e:
        print(e)
    for key,val in files.items():
        try:
            sf = GigFile()
            sf.servicefile = val
            sf.service = service
            sf.save()
            filename = val.name
            sf.file_type = file_check(filename)
            sf.save()
        except Exception as e:
            pass
    data = {
    'success':True,
    'message':"Services created"}
    dump = json.dumps(data)
    messages.success(request,"Your Gig(s) have beens added")
    return HttpResponse(dump, content_type='application/json')


# @csrf_exempt
# def permit_user(request):
#     json_data = json.loads(str(request.body, encoding='utf-8'))
#     username = json_data['username']
#     user = User.objects.get(username=username)
#     user.is_superuser = True
#     user.save()
#     data = {
#     'success':True,
#     'message':"user permitted"}
#     dump = json.dumps(data)
#     return HttpResponse(dump, content_type='application/json')

# This function will match two words and check
# how similar they are by returning the ratio matched
import re

def ratio_match(user,existing):
    from difflib import SequenceMatcher as sm
    return sm(None,user,existing).ratio()

# Create your views here.
class Searcher:
    def __init__(self):
        pass

    def my_searcher(self,all_from_db,user_prov):
        my_dict = {}
        for index,each in enumerate(all_from_db):
            ratio = self.ratio_match(user_prov,each)
            if ratio >= .6:
                #my_dict.clear()
                my_dict[each]=ratio
        return my_dict


    def ratio_match(self,user,existing):
        from difflib import SequenceMatcher as sm
        return sm(None,user,existing).ratio()

    def my_matcher(self, all_msgs,new_msg,bot_ratio=0.5):
        my_dict = {'0':0}
        for index,each_msg in enumerate(all_msgs):
            ratio = self.ratio_match(new_msg,each_msg)
            if ratio > bot_ratio and ratio > list(my_dict.values())[0]:
                my_dict.clear()
                my_dict[each_msg]=ratio
        return my_dict


def pat_search(user,my_list):
    words = []
    my = re.compile(r'{}'.format(user),re.IGNORECASE)
    for i in my_list:
        a = my.search(i)
        if a:
            words.append(i)
            # print(a.group())
    words.sort()
    return words

# This function returns an object after
# given an attribute of that object
def getItembyService(name,array):
    for i in array:
        if i.service == name:
            return i

def getItembyCategory(name,array):
    for i in array:
        if i.category == name:
            return i

def cal_rating(ratings):
    length = len(ratings)
    total = 0.0
    if length > 0:
        for i in ratings:
            total += i
        return total/length
    else:
        return 0

def build_search_result(item):
    obj = {}
    obj['id'] = item.id
    obj['service'] = item.service
    obj['start_price'] = item.start_price
    obj['gigger'] = item.gigger.username
    obj['detail'] = item.service_detail
    obj['experience'] = item.experience
    files=[]
    for f in item.files.all():
        files.append(f.servicefile.url)
    obj['files']=files
    ratings = [r.rating for r in item.ratings.all()]
    average = cal_rating(ratings)
    no_rating = len(ratings)
    obj['rating']=average
    obj['rating_number']=no_rating
    return obj



@csrf_exempt
def search_api(request):
    json_data = json.loads(str(request.body, encoding='utf-8'))
    q = json_data['q']
    cat = json_data['category']
    try:
        user = CustomUser.objects.get(username=json_data['user'])
    except:
        services = Gig.objects.all()
        service_names = [i.service for i in services]
        # print("no user")
    else:
        # print(user)
        services = Gig.objects.all()
        service_names = [i.service for i in services if i.gigger.username != user.username]
    service_cats = []
    # getting categories of the services
    for each in services:
        for c in each.categories.all():
            service_cats.append(c.name)
    if len(service_names) > 0:
        # let's do a pattern search first 
        pat_result_names = pat_search(q,service_names)
        result_names = [i for i in service_names if ratio_match(i,q) >= 0.5]
        result_names.extend(pat_result_names)
    else:
        result_names = []
    if len(service_cats) > 0:
        pat_cat_names = pat_search(q,service_cats)
        # print(pat_cat_names)
        cat_names = [i for i in service_cats if ratio_match(i,cat) >= 0.5]
        cat_names.extend(pat_cat_names)
    else:
        cat_names = []
    # adding up search word list and category list
    result_names.extend(cat_names)
    # removing duplicates
    all_names = list(set(result_names))
    objects = []
    for i in all_names:
        item = getItembyService(i,services)
        if not item:
            items = services.filter(category=i)
            for item in items:
                obj = build_search_result(item)
                objects.append(obj)
        else:
            obj = build_search_result(item)
            objects.append(obj)
    data = {'success':True,'objects':objects}
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')


def gen_order_no(number):
    if number > 0:
        no = str(number+1)
    else:
        no = str(1)
    return "#"+no.rjust(12, '0')


@csrf_exempt
def create_order(request):
    """
    {"gigs":[{"41":1}],
    "plan":{"id":"2","name":"Standard","price":"125.0",
    "description":"Reduce delivery time and more revisions","delivery_time":"5"},
    "extras":["1"],"total":175,"delivery_time":3}
    """
    json_data = json.loads(str(request.body, encoding='utf-8'))
    body = {}
    for key,val in json_data.items():
        body[key]=val
    try:
        user = CustomUser.objects.get(username=body['user'])
    except:
        # we cannot do anything here
        data = {
            "success":False,
            "message":"User is not recognised"
        }
        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')

    credit = user.credit
    no_orders = len(Order.objects.all())
    order = Order()
    order.order_no = gen_order_no(no_orders)
    order.order_by = user
    order.delivery_time = body['delivery_time']
    today = date.today()
    exp_date = today + timedelta(int(order.delivery_time))
    order.status = "Pending"
    # order.save()
    for g in body['gigs']:
        for key,val in g.items():
            try:
                gig = Gig.objects.get(id=int(key))
            except Exception as e:
                data = {'success':False,'message':str(e)}
            else:
                if credit.current_bal >= float(body['total']):
                    order.save()
                    order.gigs.add(gig)
                    order.save()
                else:
                    bal = float(body['total']) - credit.current_bal
                    data = {"success":False,"message":"You do not have enough funds. You need at least GHC {}".format(str(bal))}
                    dump = json.dumps(data)
                    return HttpResponse(dump, content_type='application/json')
    # let's work on prices now
    subtotal = 0
    c_plan = body['plan']
    plan = GigPlan.objects.get(id=int(c_plan['id']))
    order.plan = plan
    order.save()
    subtotal += plan.price
    for extra in body['extras']:
        gig_extra = Extra.objects.get(id=int(extra))
        order.extras.add(gig_extra)
        order.save()
        subtotal += gig_extra.price
    order.order_price = subtotal
    order.save()
    VAT = 0.0
    commission = 0.0
    total = VAT + commission + subtotal
    order.total_price = total
    order.save()
    credit.current_bal -= float(total)
    credit.save()
    # is there any tax or commission?
    info = {"order_no":order.order_no,
    "total_price":order.total_price,
    "VAT":order.VAT,
    "sub_total":order.order_price,"id":order.id}
    try:
        custom = body['custom']
    except:
        data={"success":True,"message":"Order created","data":info}
        # TODO:notify the gigger
    else:
        custom_order = Customization()
        custom.total_price = custom['price']
        custom.VAT = custom['vat']
        custom.commission = custom['commission']
        custom_order.save()
        custom_order.order = order
        custom_order.save()
        data={"success":True,"message":"Custom order created","data":info}
        # TODO:notify the gigger
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')


# Create Request if there are no gigs like that
@csrf_exempt
def create_request(request):
    json_data = json.loads(str(request.body, encoding='utf-8'))
    body = {}
    for key,val in json_data.items():
        body[key]=val
    try:
        user = CustomUser.objects.get(username=body['user'])
    except:
        # we cannot do anything here
        data = {
            "success":False,
            "message":"User is not recognised"
        }
        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')
    try:
        cat = GiggerCategory.objects.get(name=body['category'])
    except:
        data = {
            "success":False,
            "message":"User is not recognised"
        }
        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')
    req = Request()
    req.detail = body['detail']
    req.request = body['request']
    req.created_by = user
    req.request_by = user
    req.save()
    req.category = cat
    req.save()
    data = {
        'success':True,
        'message':'Request has been sent to giggers'
    }
    # TODO: send mail or notification to users
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')