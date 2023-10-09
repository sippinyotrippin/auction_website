from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass


class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return self.category_name


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    current_price = models.FloatField()
    image_URL = models.CharField(max_length=1000)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="user_watchlist")
    create_datetime = models.DateTimeField()

    def __str__(self):
        return self.title


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True)
    price = models.FloatField()

    def __str__(self):
        return f"{self.item}: {self.price}$"


class Comment(models.Model):
    user = models.CharField(max_length=64)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True)
    content = models.CharField(max_length=200, blank=True, null=True)
    posting_time = models.DateTimeField()

    def __str__(self):
        return f"{self.user} on {self.item}"
