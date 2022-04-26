from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from Project1.wiki.encyclopedia.forms import EditForm
from Project1.wiki.encyclopedia.views import title
from .forms import NewAuctionForm
from .models import User, Listing


def index(request):
    products_list = Listing.objects.all().order_by('-id')
    return render(request, "auctions/index.html", {
        "products_list" : products_list,
    })
    
def auction_page(request, pk):
    return render(request, "auctions/auction.html", {
        "product": Listing.objects.get(pk=pk)
    })

def create_page(request):
    form = NewAuctionForm()
    form.fields['author'].initial = User.objects.get(username=request.user).username
    if request.method == "POST":
        form = NewAuctionForm(request.POST)
        if form.is_valid():
            print(f"{form.cleaned_date['title']}")
            
    if request.user.is_authenticated:
        return render(request, "auctions/createpage.html", {
            "form": form,
        })
    return HttpResponseRedirect(reverse("login"))


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
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
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

