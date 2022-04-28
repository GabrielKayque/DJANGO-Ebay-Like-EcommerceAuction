from django.contrib import admin
from .models import Category, Listing, User, Watchlist

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    filter_horizontal = ("categories",)

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Watchlist)