from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction/<int:pk>", views.auction_page, name="auction-page"),
    # path("auction/<str:username>/new_auction", views.create_page, name="createpage"),
]
