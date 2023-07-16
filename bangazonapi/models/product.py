from django.db import models
from .category import Category
from .user import User

class Product(models.Model):
  
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=7,decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.CharField(max_length=300)
