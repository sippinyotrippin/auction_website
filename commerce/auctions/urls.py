from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing/", views.create, name="create"),
    path("listings/<int:listing_id>", views.listing_page, name="page"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("remove_from_watchlist/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("add_to_watchlist/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("categories", views.categories, name="categories"),
    path("sort_by_categories", views.index_sorted_by_categories, name="sort_by_categories"),
    path("edit_listing", views.edit_listing, name="edit_listing"),
    path("save_editing/<int:listing_id>", views.save_editing, name="save_editing"),
    path("place_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close")
]
