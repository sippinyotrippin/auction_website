from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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
            create_datetime=datetime.now()
        )
        new_listing.save()
        return HttpResponseRedirect(reverse("index"))


def listing_page(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    is_in_watchlist = request.user in listing.watchlist.all()
    is_it_owner = request.user == listing.owner or request.user.is_superuser
    return render(request, "auctions/listing_page.html", {
        "item": listing,
        "is_in_watchlist": is_in_watchlist,
        "is_it_owner": is_it_owner,
        "bid_message": "",
        "bids_amount": len(Bid.objects.filter(item=listing_id)),
        'is_owner_to_close': request.user == listing.owner
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
        category_id = Category.objects.get(category_name=selected_category).id
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category=category_id)
    })


def edit_listing(request):
    current_id = request.GET.get('id_')
    title = request.GET.get('title_')
    description = request.GET.get('description_')
    image = request.GET.get('image_')
    price = request.GET.get('price_')
    return render(request, "auctions/edit_listing.html", {
        "listing_id": current_id,
        "title": title,
        "description": description,
        "image": image,
        "price": price,
        "categories": Category.objects.all()
    })


def save_editing(request, listing_id):
    new_title = request.POST.get('title')
    new_description = request.POST.get('description')
    new_image = request.POST.get('image_url')
    new_price = request.POST.get('price')

    changes = (new_title, new_description, new_image, new_price)

    Listing.objects.filter(pk=listing_id).update(title=new_title)
    Listing.objects.filter(pk=listing_id).update(description=new_description)
    Listing.objects.filter(pk=listing_id).update(image_URL=new_image)
    Listing.objects.filter(pk=listing_id).update(current_price=new_price)
    Listing.objects.filter(pk=listing_id).update(create_datetime=datetime.now())
    return HttpResponseRedirect(reverse("page", args=(listing_id, )))


def place_bid(request, listing_id):
    suggested_price = int(request.POST.get('bid'))
    listing = Listing.objects.get(pk=listing_id)
    is_in_watchlist = request.user in listing.watchlist.all()
    is_it_owner = request.user == listing.owner or request.user.is_superuser
    if suggested_price > listing.current_price:
        your_bid = Bid(
            user=request.user,
            item=Listing.objects.get(pk=listing_id),
            price=suggested_price
        )
        your_bid.save()
        Listing.objects.filter(pk=listing_id).update(current_price=your_bid.price)
        return HttpResponseRedirect(reverse("page", args=(listing_id, )))
    else:
        message = "Your bid must be larger than the current price"
        return render(request, "auctions/listing_page.html", {
            "item": listing,
            "is_in_watchlist": is_in_watchlist,
            "is_it_owner": is_it_owner,
            "bid_message": message,
            "bids_amount": len(Bid.objects.filter(item=listing_id)),
        })


def add_comment(request, listing_id):
    your_comment = Comment(
        user=request.user,
        item=Listing.objects.get(pk=listing_id),
        content=request.POST.get('content'),
        posting_time=datetime.now()
    )
    your_comment.save()
    return HttpResponseRedirect(reverse('page', args=(listing_id, )))


def close_auction(request, listing_id):
    bid_info = Bid.objects.filter(item=listing_id)
    best_bid = bid_info[len(bid_info)-1]
    winner = best_bid.user
    listing = Listing.objects.filter(pk=listing_id).update(is_active=False)
    listing.watchlist.clear()
