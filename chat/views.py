from django.shortcuts import render, redirect, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.contrib import messages
from datetime import datetime,date, timedelta
from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from django.db.models.fields.files import ImageFieldFile
from django.apps import apps
from accounts.models import CustomUser
from gigs.models import Order


models = apps.get_app_config('chat').get_models()
objects = {}
for model in models:
    objects[model.__name__]=model

class ExtendedEncoder(DjangoJSONEncoder):

    def default(self, o):
        if isinstance(o, ImageFieldFile):
            try:
                mypath = o.path
            except:
                return ''
            else:
                return mypath
        # this will either recusively return all atrributes of the object or return just the id
        elif isinstance(o, Model):
            # return model_to_dict(o)
            return o.id

        return super().default(o)

class ExtendedEncoderAllFields(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, ImageFieldFile):
            try:
                mypath = o.path
            except:
                return ''
            else:
                return mypath
        # this will either recusively return all atrributes of the object or return just the id
        elif isinstance(o, Model):
            return model_to_dict(o)
            # return o.id

        return super().default(o)

def getRelatedName(model,field):
    "Get the model to which a field is related"
    return model._meta.get_field(field).related_model.__name__


def raltionship(model,field):
    "What relationship does this field hold"
    if model._meta.get_field(field).many_to_one:
        return "many_to_one"
    elif model._meta.get_field(field).many_to_many:
        return "many_to_many"
    elif model._meta.get_field(field).one_to_one:
        return "one_to_one"
    elif model._meta.get_field(field).one_to_many:
        return "one_to_many"
    else:
        return "no_relation"

class Activity:
    # class constructor, initializer
    def __init__(self,modelName):
        self.modelName = modelName
        self.objects = objects

    # class method
    def create(self,**kwargs):
        # model = apps.get_model('Accounts', self.modelName)
        try:
            # creating instance as django model object based on passed modelName string
            instance = self.objects[self.modelName]()
            instance.save()
            # This error may usually be KeyError
        except Exception as e:
            return {'success':False,'message':str(e)}
        else:
            # Now, let's use passed keyword arguments to set field values for our instance
            for key,val in kwargs.items():
                try:
                    main = self.modelName
                    if raltionship(self.objects[main],key) == "many_to_one":
                        # TODO: create new objects recersively from relations
                        try:
                            rel_name = getRelatedName(self.objects[main],key)
                            child_model = self.objects[rel_name]
                            children = child_model.objects.get(id=int(val))
                        except Exception as e:
                            pass
                            # return {'success':False,'message':str(e)}
                        else:
                            try:
                                instance.__setattr__(key,children)
                            except Exception as e:
                                return {'success':False,'message':str(e)}
                            else:
                                try:
                                    instance.save()
                                except Exception as e:
                                    return {'success':False,'message':str(e)}
                    # is the field a many to many key
                    elif raltionship(self.objects[self.modelName],key) == "many_to_many":
                        try:
                            rel_name = getRelatedName(self.objects[main],key)
                            child_model = self.objects[rel_name]
                            children = [child_model.objects.get(id=int(i)) for i in val]
                        except Exception as e:
                            return {'success':False,'message':str(e)}
                        else:
                            try:
                                # field = self.objects[self.modelName]._meta.get_field(key)
                                # field.set(children)
                                # instance.__setattr__(key,children)
                                if key == "tests_available":
                                    instance.tests_available.add(*children)
                            except Exception as e:
                                return {'success':False,'message':str(e)}
                            else:
                                try:
                                    instance.save()
                                except Exception as e:
                                    return {'success':False,'message':str(e)}
                    else:
                        try:
                            instance.__setattr__(key,val)
                        except Exception as e:
                            return {'success':False,'message':str(e)}
                except:
                    pass
                    # # is the field a foreign key
                    # main = self.modelName
                    # if raltionship(self.objects[main],key) == "many_to_one":
                    #     # TODO: create new objects recersively from relations
                    #     try:
                    #         rel_name = getRelatedName(self.objects[main],key)
                    #         child_model = self.objects[rel_name]
                    #         children = child_model.objects.get(id=int(val))
                    #     except Exception as e:
                    #         return {'success':False,'message':str(e)}
                    #     try:
                    #         instance.__setattr__(key,children)
                    #     except Exception as e:
                    #         return {'success':False,'message':str(e)}
                    #     instance.save()
                    # # is the field a many to many key
                    # if raltionship(self.objects[self.modelName],key) == "many_to_many":
                    #     try:
                    #         rel_name = getRelatedName(self.objects[self.modelName],key)
                    #         child_model = self.objects[rel_name]
                    #         children = [child_model.objects.get(id=int(i)) for i in val]
                    #     except Exception as e:
                    #         return {'success':False,'message':str(e)}
                    #     instance.save()
                    # try:
                    #     instance.__setattr__(key,children)
                    # except Exception as e:
                    #     return {'success':False,'message':str(e)}
                    # instance.save()
                else:
                    instance.save()
                 # is the field a foreign key

            # try:
            #     instance.__setattr__(key,children)
            # except Exception as e:
            #     return {'success':False,'message':str(e)}
            # instance.save()
        # adding parents to the object (may be more than one parent
        # if parents:
        #     for parent in parents:
        #         try:
        #             parent = parent['name']
        #             instance.__setattr__(parent,parent['value'])
        #             instance.save()
        #         except:
        #             pass
        return {'success':True,'message':'successful','data':instance}

    # reads from database the particular model instance given
    # TODO: add specific field to be returned as **kwargs
    def read(self,key_id,primary_key,*fields):
        # setting the model based on passed model string
        # and getting all fields of the model
        allfields = self.objects[self.modelName]._meta.get_fields()
        # setting instance as passed instance
        instance = self.objects[self.modelName].__getattr__.get(key_id,primary_key)
        names = []
        vals = []
        # here we get all the available fields on a particular instance
        # this means if the field is not yet created but exists on the model, it will not be taken
        objects = {}
        # This will use user defined field when return the object requested
        if fields:
            for field in fields:
                try:
                    val = (getattr(instance, field))
                except:
                    pass
                else:
                    names.append(field)
                    try:
                        obj = list(val.values())
                    except:
                        vals.append(val)
                    else:
                        vals.append(obj)
            for i,e in enumerate(names):
                objects[e]=vals[i]

        else:
            # this will return all available fields on the instance
            for field in allfields:
                try:
                    val = (getattr(instance, field.name))
                except:
                    pass
                else:
                    names.append(field.name)
                    try:
                        obj = list(val.values())
                    except:
                        vals.append(val)
                    else:
                        vals.append(obj)
            for i,e in enumerate(names):
                objects[e]=vals[i]
            # our return dictionary contains fields with their values even ManyToMany or related field
            # Already serialized
        dump = json.dumps(objects,cls=ExtendedEncoder)
        return {'success':True,'data':dump}

    # class method to update object
    def update(self,key_id,primary_key,**kwargs):
        try:
            instance = self.objects[self.modelName].__getattr__.get(key_id,primary_key)
        except Exception as e:
            return False
        else:
            for key,val in kwargs.items():
                try:
                    instance.__setattr__(key,val)
                except:
                    pass
            instance.save()
        return {'success':True}


    # class method to delete instance of the model
    def delete(self,key_id,primary_key):
        try:
            instance = self.objects[self.modelName].__getattr__.get(key_id,primary_key)
        except Exception as e:
            return False
        else:
            instance.delete()
            return {'success':True}



def get_args(user,page):
    args = {}
    if page == "my-order":
        orders = Order.objects.all()
        gigs = [i.gigs.all() for i in orders]
        args['orders'] = [i for i in orders if user in gigs]
    return args

def chunkList(lst,n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

# Create your views here.
def chat(request):
    template_name = "chat/chat.html"
    args = {}
    return render(request, template_name, args)


@csrf_exempt
def getPeople(request):
    try:
        json_data = json.loads(str(request.body, encoding='utf-8'))
        user = CustomUser.objects.get(username=json_data['username'])
        orders = Order.objects.filter(order_by=user)
        orders = [i for i in orders]
        orders.extend(Order.objects.filter(order_to=user))
        people = [i.order_by for i in orders]
        people.extend([i.order_to for i in orders])
        people = list(set(people))
    except Exception as e:
        data = {'success':False,'message':str(e)}
    else:
        try:
            people.remove(user)
        except:
            pass
        # now lets get their basic info
        objects = []
        for person in people:
            obj = {}
            obj['username']=person.username
            if person.user_img:
                obj['image']="/"+str(person.user_img.url)
            else:
                obj['image']="/static/images/svgs/jobs/work.svg"
            # TODO: Get the online status here
            try:
                msg = Message.objects.filter(from_user=person)[0]
            except:
                ob = {}
                ob['content'] = "Hello, I am "+str(person.username)
                ob['time']=datetime.now()
                ob['count']=1
                obj['lastMsg']=ob
            else:
                ob = {}
                ob['content']=msg.content
                ob['time']=msg.date_created
                ob['count'] = len(Message.objects.filter(from_user=person))
                obj['lastMsg']=ob
                
            objects.append(obj)
        data = {'success':True,'objects':objects}
    dump = json.dumps(data,cls=ExtendedEncoderAllFields)
    return HttpResponse(dump, content_type='application/json')


@csrf_exempt
def getMessages(request):
    json_data = json.loads(str(request.body, encoding='utf-8'))
    user = CustomUser.objects.get(username=json_data['thisuser'])
    other = CustomUser.objects.get(username=json_data['otheruser'])
    page = int(json_data['page'])
    try:
        msgs = Message.objects.filter(from_user=user,to_user=other)|Message.objects.filter(to_user=user,from_user=other)
    except Exception as e:
        data = {"success":False,"message":str(e)}
    else:  
        chunks = chunkList(msgs,10)
        try:
            chunked = chunks[page-1]
        except:
            try:
                chunked = chunks[-1]
            except:
                chunked = []
        data = {"success":True,"objects":chunked}
    dump = json.dumps(data,cls=ExtendedEncoderAllFields)
    return HttpResponse(dump, content_type='application/json')