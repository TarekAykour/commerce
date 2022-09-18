
from datetime import date, datetime
from turtle import update
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import Create, AddComment, AddBid
from .models import User, Listing, Comment, Bid, Category
from django.contrib.auth.decorators import login_required
from django.db.models import Max




def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="/login")
def create(request):
    watchers = request.user.listings.all()
    form = Create()
    if request.method == "POST":
        form = Create(request.POST, request.FILES)
        if form.is_valid():
            print(form.errors)
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            image = form.cleaned_data["image"]
            price = form.cleaned_data["price"]
            category = form.cleaned_data["category"]
            
            l = Listing(user=request.user,title=title, description=description, image=image, price=price, category=category)
            l.save()
            return HttpResponseRedirect("/")
        else:

            return render(request,"auctions/error.html", {
                "error": form.errors
            })
    else: 
        return render(request, "auctions/create.html", {
            "form": form,
            "watchers": watchers
           
        })

# listing page
@login_required(login_url='/login')
def listing(request, id):
    comment_form = AddComment()
    bid_form = AddBid()
    listing =  Listing.objects.get(id=id)
    if not listing:
        return HttpResponseRedirect("/")
    
    watchers = request.user.listings.all()
    bids = Bid.objects.filter(listing_id=listing.id)
    comments = Comment.objects.filter(listing_id=listing.id)
    winner = None
    for bid in Bid.objects.filter(listing_id=listing.id).values_list("amount"):
        if listing.is_active == False:
            if bids.aggregate(Max('amount'))['amount__max'] == bid[0]:
                winner = Bid.objects.get(listing_id=listing.id, amount=bids.aggregate(Max('amount'))['amount__max']).user

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comment_form": comment_form,
        "bid_form": bid_form,
        "watchers": watchers,
        "bids": bids,
        "comments": comments,
        "winner": winner
    })

# add watch list
@login_required
def deletewatchlist(request,id):
    listings = Listing.objects.get(id=id)
    listings.watchers.remove(request.user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


# add watch list
@login_required
def addwatchlist(request,id):
    listings = Listing.objects.get(id=id)
    listings.watchers.add(request.user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

# watchlist

@login_required(login_url='/login')
def watchlist(request):
    listings = request.user.listings.all()
    watchers = request.user.listings.all()
    return render(request,"auctions/watchlist.html", {
        "listings": listings,
        "watchers": watchers
    })


@login_required
def addbid(request,id):
    listing = Listing.objects.get(id=id)
    amount = float(request.POST.get("amount")) 
    comment_form = AddComment()
    bid_form = AddBid()
    listing =  Listing.objects.get(id=id)
    watchers = request.user.listings.all()
    bids = Bid.objects.filter(listing_id=listing.id)
    comments = Comment.objects.filter(listing_id=listing.id)
    if amount is not None:
        if amount > listing.price:
            b = Bid(user=request.user,amount=amount,listing=listing)
            b.save()
            listing.price = b.amount
            listing.save()
            updated = True
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "Bid has been updated",
                "comment_form": comment_form,
                "bid_form": bid_form,
                "watchers": watchers,
                "bids": bids,
                "comments": comments,
                "updated": updated
                 
            })
        else:
            updated = False
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "message": "Bid too low!",
                "comment_form": comment_form,
                "bid_form": bid_form,
                "watchers": watchers,
                "bids": bids,
                "comments": comments,
                "updated": updated
            } )
        
    
        
       
   


@login_required
def addcommment(request,id):
    listing = Listing.objects.get(id=id)
    comment = request.POST.get("comment")
    if comment is not None:
        c = Comment(user=request.user,comment=comment,listing=listing,date=datetime.now())
        c.save()
        return HttpResponseRedirect(reverse("listing", args=(id, )))
    else:
        return HttpResponseRedirect(reverse("listing", args=(id, )))
        



def categories(request):
    categories = list(Category.objects.all())
    listings = Listing.objects.all()
    # list(categories).index(category)
    if request.method == "POST":
        
        categoryform = request.POST['category']
        category = Category.objects.get(category=categoryform)
        listing = Listing.objects.filter(category=category)
        print(listing)
        return render(request, "auctions/categories.html", {
            "categories": categories,
            "listings": listing
        })
    else:   
        return render(request, "auctions/categories.html", {
            "categories": categories,
            "listings": listings
        })

@login_required
def closeauction(request,id):
    listing = Listing.objects.get(id=id)
    listing.is_active = False
    listing.save(update_fields=['is_active'])
    return HttpResponseRedirect(reverse("listing", args=(id, )))

@login_required
def openauction(request,id):
    listing = Listing.objects.get(id=id)
    listing.is_active = True
    listing.save(update_fields=['is_active'])
    return HttpResponseRedirect(reverse("listing", args=(id, )))

@login_required
def deleteauction(request,id):
    listing = Listing.objects.get(id=id)
    listing.delete()
    return HttpResponseRedirect(reverse("index"))

