from django.db import models
import os
from mysite.settings import MEDIA_ROOT
from core.models import Orders, Product
# from django.db.models import JSONField


# Create your models here.
class users(models.Model):
    image = models.ImageField(upload_to=os.path.join(MEDIA_ROOT, "consumer/images"), null=True, blank=True)
    name = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=100)
    contact = models.IntegerField(unique=True, null=True, blank=True)
    sessionID = models.CharField(max_length=36, null=True, blank=True)
    address = models.JSONField(default=list, blank=True)
    # city = models.CharField(max_length=50)
    # district = models.CharField(max_length=50)
    # state = models.CharField(max_length=50)
    # pincode = models.CharField(max_length=6)
    createOn = models.DateTimeField(auto_now_add=True)
    lastLogin = models.DateTimeField(auto_now=True)


    order = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    
    SHIPMENT_TYPE ={
        "s": "Standart",
        "e": "Express",
    }

    PAYMENT_TYPES = {
        "p": "Pay on Delivery",
        "c": "Credit/Debit Card",
        "u": "UPI",
    }

    price = models.IntegerField(blank=True, default=0)
    user = models.ForeignKey(users, on_delete=models.CASCADE, unique=True)
    # shipment = models.CharField(choices = SHIPMENT_TYPE, max_length=1, default="s")
    products = models.JSONField(default=list, blank=True)
    # products = models.ForeignKey(Product, on_delete=models.CASCADE)