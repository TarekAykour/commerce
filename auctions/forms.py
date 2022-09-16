from secrets import choice
from .models import Listing, Comment, Bid,Category
from django.forms import ModelForm
from django import forms

class Create(ModelForm):
   class Meta:
        model = Listing
        fields = ['title', 'description', 'image', 'price', 'category']
      


   
class AddComment(ModelForm):
       class Meta:
             model = Comment
             fields = ['comment']


class AddBid(ModelForm):
       class Meta:
             model = Bid
             fields = ['amount']
