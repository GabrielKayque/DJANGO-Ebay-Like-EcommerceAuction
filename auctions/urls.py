from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction/new_auction", views.create_page, name="createpage"),
    path("auction/<int:pk>", views.auction_page, name="auction-page"),
    path("auction/<int:pk>/addtowatchlist", views.add_watchlist, name="watchlist"),
    path("auction/watchlist", views.watchlist_page, name="watchlist-page"),
]
