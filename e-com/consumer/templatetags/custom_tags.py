# dinosoar/dinofacts/templatetags/dinotags.py

from django import template
from types import SimpleNamespace
from core.models import Orders
from core.models import Product
from consumer.models import users
import locale
import json

from datetime import datetime

register = template.Library()

# class Dictionary:
#     def __init__(self, dict):
#         print(dict)
#         self.__dict__.update(dict)



@register.filter
def make_obj(dict):
    obj = SimpleNamespace(**dict)
    # obj = Dictionary(dict)
    return obj

@register.filter
def format_inr(amount):
    # Set locale to India
    locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
    
    # Format the amount using the locale for INR
    formatted_amount = locale.currency(amount, grouping=True)
    return formatted_amount

@register.filter
def get_product_from_id(id):
    product = Product.objects.get(id = id)
    return product

@register.filter
def get_order_from_id(orderID):
    order = Orders.objects.get(orderID = orderID)
    return order



# @register.filter
# def get_address_from_id(userID, addressID):
#     user = users.objects.get(id = userID)
#     # for i in user.address:

#     return "order"
