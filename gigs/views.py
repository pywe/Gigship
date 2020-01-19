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
