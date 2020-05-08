from django.db import models
from django.conf import settings

# Create your models here.
class Message(models.Model):
    content = models.TextField(null=True,blank=True)
    date_created = models.DateTimeField(null=True,blank=True,auto_now_add=True)
    date = models.DateField(null=True,blank=True,auto_now_add=True)
    time = models.TimeField(null=True,blank=True,auto_now_add=True)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank = True, on_delete = models.SET_NULL,related_name="to_user")
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank = True, on_delete = models.SET_NULL,related_name="from_user")
    sent = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    reply = models.ForeignKey("self",null=True, blank = True, on_delete = models.SET_NULL)


    def __str__(self):
        return "from {} to {}".format(str(self.from_user.username),str(self.to_user.username))


class MessageFile(models.Model):
    message = models.ForeignKey(Message,null=True, blank = True, on_delete = models.SET_NULL,related_name="files")
    name = models.CharField(max_length=50,null=True,blank=True)
    message_file = models.FileField(null=True,upload_to="static/messages/")
    date_created = models.DateTimeField(null=True,blank=True,auto_now_add=True)
