from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name
    
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
    name=models.CharField(max_length=100,blank=True)
    gmail=models.EmailField(blank=True)
    phonenumber=models.CharField(max_length=15,blank=True)

    def _str_(self):
        return self.username