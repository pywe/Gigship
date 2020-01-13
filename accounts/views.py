from django.shortcuts import render

# Create your views here.
# index page, showing homepage to users
def index(request):
    template_name = "accounts/index.html"
    args = {}
    return render(request,template_name,args)