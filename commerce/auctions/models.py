from django.contrib.auth.models import AbstractUser
from django.db import models


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
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="category")

    def __str__(self):
        return self.title


class Bid(models.Model):
    pass


class Comment(models.Model):
    pass
