from traceback import print_tb
from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.user


class Box(models.Model):
    Height = models.IntegerField(null=True,blank=True)
    Length=models.IntegerField(null=True,blank=True)
    Width=models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Creator=models.ForeignKey(Account,null=True,blank=True,on_delete=models.SET_NULL)
    Area=models.IntegerField(null=True,blank=True)
    Volume=models.IntegerField(null=True,blank=True)

    def get_Area(self):
        print(self.Height)
        print(self.Length)
        print(self.Width)
        area=(int(self.Height)*int(self.Length)+int(self.Length)*int(self.Width)+int(self.Width)*int(self.Height))*2
        return area

    def get_Volume(self):
        volume=(int(self.Height)*int(self.Length)*int(self.Width))
        return volume
    
    def save(self, *args, **kwargs):
       self.Area = self.get_Area()
       self.Volume=self.get_Volume()
       super(Box, self).save(*args, **kwargs)
