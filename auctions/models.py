from datetime import datetime
from time import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=200)
    def __str__(self):
        return self.category





class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, default='',  null=True )
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='media/')
    price = models.FloatField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default='',blank=True, null=True)
    # a listing can have multiple watchers and a watcher can have multiple listings
    watchers = models.ManyToManyField(User,blank=True,related_name="listings",default=None)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return "%s" % (self.title)




class Bid(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default='')
    
    def __str__(self):
        return "%s: %s - %s" % (self.listing, self.user, self.amount)
    

# comment
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, default='')
    date = models.DateField(default=now)
    def __str__(self):
        return "%s %s" % (self.user, self.comment)









