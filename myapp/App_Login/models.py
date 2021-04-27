from django.db import models

#To Create A Custom User Model and admin panel
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.utils.translation import ugettext_lazy

import uuid



# Create your models here.

class MyuserManager(BaseUserManager): #To Manage new users using this baseusermanaegr class
    """ A Custom User Manager to deal with Emails  as an unique Identifier """
    def _create_user(self,email,username,password,**extra_fields):
        """Creates and Saves an user with given email and password """ 
        
        if not email:
            raise ValueError('Email Must Be Set')
        
        email=self.normalize_email(email)
        user=self.model(email=email,username=username,**extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self,email,username,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('SuperUser is_staff must be True')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('SuperUser is_superuser must be True')
        
        return self._create_user(email,username,password,**extra_fields) 
    
    
    
class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True,null=False)
    username=models.CharField(max_length=264)
    is_merchant=models.BooleanField(default=False)
    is_staff=models.BooleanField(
        ugettext_lazy('staff_status'),default=False,help_text='Determines Whether They Can Log in this Site or not'
    )    
    is_active=models.BooleanField(
        ugettext_lazy('active'),default=True,help_text='Determines Whether their Account Status is Active or not'
    )    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    objects=MyuserManager()
    
    class Meta:
        verbose_name_plural='User'
        db_table = 'User'
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username
    
    

class Merchant(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='merchant')  
    full_name=models.CharField(max_length=264,blank=True)
    address_1=models.TextField(max_length=264,blank=True)
    phone=models.CharField(max_length=20,blank=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    invoice_id=models.CharField(unique=True,max_length=10)    
    class Meta:
        verbose_name_plural='Merchant'
        db_table = 'Merchant'

    def __str__(self):
        return u'{0}'.format(self.user.username)
    
    def is_fully_filled(self):
        fields_name=[f.name for f in self._meta.get_fields()]
        
        for fields in fields_name:
            value=getattr(self,fields)
            if value is None or value=='':
                return False
        return True
        
    
    
