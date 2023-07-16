from django.db import models
from .user import User

class Order(models.Model):

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=7,decimal_places=2)
    payment_type = models.CharField(max_length=50)
    
