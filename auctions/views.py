
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import Create, AddComment, AddBid
from .models import User, Listing, Comment, Bid, Category
from django.contrib.auth.decorators import login_required


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
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
           
        })

# listing page

def listing(request, id):
    comment_form = AddComment()
    bid_form = AddBid()
    listing =  Listing.objects.get(id=id)
    watchers = request.user.listings.all()
    bids = Bid.objects.filter(listing_id=listing.id)
    comments = Comment.objects.filter(listing_id=listing.id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "comment_form": comment_form,
        "bid_form": bid_form,
        "watchers": watchers,
        "bids": bids,
        "comments": comments
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
    return render(request,"auctions/watchlist.html", {
        "listings": listings
    })


@login_required
def addbid(request,id):
    listing = Listing.objects.get(id=id)
    amount = float(request.POST.get("amount"))
    if amount is not None:
        if amount >= listing.price:
            b = Bid(user=request.user,amount=amount,listing=listing)
            b.save()
            return HttpResponseRedirect(reverse("listing", args=(id, )))
        else:
            return HttpResponseRedirect(reverse("listing", args=(id, )))


@login_required
def addcommment(request,id):
    listing = Listing.objects.get(id=id)
    comment = request.POST.get("comment")
    if comment is not None:
        c = Comment(user=request.user,comment=comment,listing=listing)
        c.save()
        return HttpResponseRedirect(reverse("listing", args=(id, )))
    else:
        return HttpResponseRedirect(reverse("listing", args=(id, )))
        
    