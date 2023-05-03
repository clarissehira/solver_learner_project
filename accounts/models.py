from django.db import models
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token

class User(AbstractUser):
    is_instructor=models.BooleanField(default=False)
    is_student=models.BooleanField(default=False)
    
    def __str__(self):
     return self.username
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None,created=False, **kwargs ):
    if created:
        Token.objects.create(user=instance)        

class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="instructor")
    first_name= models.CharField(max_length=70, blank=True)
    last_name = models.CharField(max_length=70, blank=True)
    username = models.CharField(max_length=70, unique=True)
    phone=models.CharField(max_length=40, blank=True)
    email=models.EmailField()
    course=models.CharField(max_length=30, blank=True)     

    def __str__(self):
        return f"{self.first_name} {self.last_name}"




class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="students")
    first_name=models.CharField(max_length=40,blank=True)
    last_name=models.CharField(max_length=40,blank=True)
    email=models.EmailField()
    
       
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"



