from django.db import models

class User(models.Model):
  
    uid = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
