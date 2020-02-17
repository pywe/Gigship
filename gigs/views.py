from django.shortcuts import render,redirect,HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from accounts.models import CustomUser
from .models import *


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
    ids = []
    services = json_data['services']
    username = json_data['username']
    user = CustomUser.objects.get(username=username)
    for s in services:
        service = s['service']
        start_price = s['start_price']
        category = s['category']
        experience = s['experience']
        service_detail = s['service_detail']
        myservice = Service()
        myservice.service = service
        myservice.start_price = start_price
        myservice.category = category
        myservice.experience = experience
        myservice.service_detail = service_detail
        myservice.save()
        myservice.gig = user
        myservice.save()
        ids.append(myservice.id)
    data = {
    'success':True,
    'message':"Services created",
    "services":ids}
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')

@csrf_exempt
def add_service_files(request,id):
    files = request.FILES.getlist('files')
    service = Service.objects.get(ide=int(id))
    for f in files:
        sf = ServiceFile()
        sf.servicefile = f
        sf.service = service
        sf.save()
    data = {
    'success':True,
    'message':"Services created"}
    dump = json.dumps(data)
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
def ratio_match(user,existing):
    from difflib import SequenceMatcher as sm
    return sm(None,user,existing).ratio()

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


@csrf_exempt
def search_api(request):
    json_data = json.loads(str(request.body, encoding='utf-8'))
    q = json_data['q']
    cat = json_data['category']
    services = Service.objects.all()
    service_names = [i.service for i in services]
    service_cats = [i.category for i in services]
    result_names = [i for i in service_names if ratio_match(i,q) >= 0.5]
    cat_names = [i for i in service_cats if ratio_match(i,cat) >= 0.8]
    all_names = result_names
    objects = []
    for i in all_names:
        item = getItembyService(i,services)
        if not item:
            item = getItembyCategory(i,services)
        if item:
            obj = {}
            obj['service'] = item.service
            obj['start_price'] = item.start_price
            obj['gig'] = item.gig.username
            obj['detail'] = item.service_detail
            obj['experience'] = item.experience
            objects.append(item)
    data = {
    'success':True,
    'objects':objects}
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')