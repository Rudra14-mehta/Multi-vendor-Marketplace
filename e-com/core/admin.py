from django.contrib import admin
from .models import Orders, Product

# Register your models here.
admin.site.register(Orders)
admin.site.register(Product)