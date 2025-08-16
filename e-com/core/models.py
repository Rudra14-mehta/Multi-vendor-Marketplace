from django.db import models
from seller.models import Seller
import os
from mysite.settings import MEDIA_ROOT

# Create your models here.
class countryCode(models.Model):
    country = models.CharField(max_length=100)
    dialCode = models.CharField(max_length=5)
    image = models.CharField(max_length=100)
    def __str__(self):
        return self.country
    
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ("Toys", "Toys"),
        ("Electronics", "Electronics"),
        ("Fashion", "Fashion"),
        ("Beauty And Personal Care", "Beauty And Personal Care"),
        ("Home And Furniture", "Home And Furniture"),
        ("Sports And Outdoors", "Sports And Outdoors"),
        ("Books And Stationery", "Books And Stationery"),
        ("Food And Beverages", "Food And Beverages"),
        ("Health And Medical", "Health And Medical"),
        ("Automotive And Tools", "Automotive And Tools"),
        ("Pet Supplies", "Pet Supplies"),
        ("Office Products", "Office Products"),
        ("Arts And Crafts", "Arts And Crafts"),
        ("Baby And Kids", "Baby And Kids"),
        ("Luxury And Designer", "Luxury And Designer"),
        ("Books Music And Movies", "Books Music And Movies"),
        ("Seasonal Products", "Seasonal Products"),
        ("Travel And Luggage", "Travel And Luggage"),
        ("Digital Products", "Digital Products"),
        ("Gifts And Special Occasion", "Gifts And Special Occasion"),
        ("Sustainability And Eco Friendly", "Sustainability And Eco Friendly"),
    ]

    image = models.ImageField(upload_to="products/images/", null=True, blank=True)  # This field
    name = models.CharField(max_length=250)
    sku = models.CharField(max_length=16, unique=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    addedOn = models.DateTimeField(auto_now_add=True)
    updatedOn = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.name
    

class Orders(models.Model):
    STATUS_LIST = [
        ("p", "Placed") ,
        ("pr", "Processing") ,
        ("s", "Shipped") ,
        ("d", "Delivered") ,
        ("c", "Canceled") ,
    ]

    SHIPMENT_TYPE =[
        ("s", "Standart"),
        ("e", "Express"),
    ]

    PAYMENT_TYPES = [
        ("p", "Pay on Delivery"),
        ("c", "Credit/Debit Card"),
        ("u", "UPI"),
    ]
    
    # quantity = models.IntegerField()
    orderID = models.CharField(max_length=20, unique=True)
    price = models.IntegerField()
    address = models.CharField(max_length=19)
    orderOn = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.CharField( max_length=2, choices=STATUS_LIST, default='p')
    shipment = models.CharField(choices = SHIPMENT_TYPE, max_length=1, default="s")
    paymentMethod = models.CharField(choices = PAYMENT_TYPES, max_length=1, default="p")
    products = models.JSONField(default="list", blank="True")

    # totalItems = models.IntegerField()

    # buyer = models.ForeignKey(users, on_delete=models.CASCADE)

    def __str__(self):
        return self.orderID

