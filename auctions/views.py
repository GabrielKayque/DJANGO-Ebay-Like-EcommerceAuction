from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import NewAuctionForm
from .models import User, Listing, Watchlist


def index(request):
    products_list = Listing.objects.all().order_by('-id')
    return render(request, "auctions/index.html", {
        "products_list" : products_list,
    })

@login_required(login_url='/login') 
def watchlist_page(request):
    userlist = Watchlist.objects.get(user=request.user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": userlist
    })
    
def auction_page(request, pk):
    in_watchlist = False
    product = Listing.objects.get(pk=pk)
    try:
        if Watchlist.objects.filter(user=request.user, product=product).exists():
            in_watchlist = True
    except TypeError:
        pass
    return render(request, "auctions/auction.html", {
        "product": product,
        "in_watchlist": in_watchlist,
    })

def create_page(request):
    if request.user.is_authenticated:
        form = NewAuctionForm()
        form.fields['author'].initial = User.objects.get(username=request.user)
        if request.method == "POST":
            form = NewAuctionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse("auction-page",args={Listing.objects.last().id}))
            
                
        return render(request, "auctions/createpage.html", {
            "form": form,
        })
    return HttpResponseRedirect(reverse("login"))

def add_watchlist(request, pk):
    product_to_add = get_object_or_404(Listing, id=pk)
    if Watchlist.objects.filter(user=request.user, product=product_to_add).exists():
        userlist = Watchlist.objects.get(user=request.user)
        userlist.product.remove(product_to_add)
        if request.method == "POST":
            return redirect(reverse("watchlist-page"))
        return redirect(reverse("auction-page", args={pk}))
    userlist, _ = Watchlist.objects.get_or_create(user=request.user)
    userlist.product.add(product_to_add)
    return redirect(reverse("auction-page", args={pk}))

        

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"].lower()
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
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"].lower().strip()
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

