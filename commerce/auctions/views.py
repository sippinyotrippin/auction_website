from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True)
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


def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            'categories': Category.objects.all()
        })
    else:
        title = request.POST['title']
        description = request.POST['description']
        price = request.POST['price']
        image_url = request.POST['image_url']
        category_name = request.POST['category']

        new_listing = Listing(
            title=title,
            description=description,
            current_price=float(price),
            image_URL=image_url,
            is_active=True,
            owner=request.user,
            category=Category.objects.get(category_name=category_name),
        )
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))


def listing_page(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    is_in_watchlist = request.user in listing.watchlist.all()
    return render(request, "auctions/listing_page.html", {
        "item": listing,
        "is_in_watchlist": is_in_watchlist
    })


def watchlist(request):
    current_user = request.user
    listings = current_user.user_watchlist.all()
    return render(request, "auctions/watchlist.html", {
       "listings": listings
    })


def add_to_watchlist(request, listing_id):
    current_listing = Listing.objects.get(pk=listing_id)
    current_user = request.user
    current_listing.watchlist.add(current_user)
    return HttpResponseRedirect(reverse("watchlist"))


def remove_from_watchlist(request, listing_id):
    current_listing = Listing.objects.get(pk=listing_id)
    current_user = request.user
    current_listing.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse("index"))


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def index_sorted_by_categories(request):
    if request.method == "GET":
        selected_category = request.GET["category"]
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category=selected_category)
    })
