from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=25)
    
    
class Listing(models.Model):
    title = models.CharField(max_length=64)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    description = models.TextField()
    bid = models.FloatField()
    imgurl = models.URLField()
    categories = models.ManyToManyField(Category, blank=True, related_name="listings")
    created_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} | {self.author}"
