from .models import Listing, Comment, Bid
from django.forms import ModelForm
from django import forms

class Create(forms.Form):
    title = forms.CharField(label="title", max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()
    price = forms.FloatField()

   

