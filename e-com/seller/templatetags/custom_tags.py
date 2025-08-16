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
    try:
        json_obj = json.dumps(dict)
        print(json_obj)
        return json_obj
    except (TypeError, ValueError) as e:
        print(f"Error converting dict to JSON: {e}")
        return None


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
@register.filter
def jsonify(value):
    """Convert a Python object to a JSON string."""
    return json.dumps(value)

@register.filter
def format_price(value):
    """Ensure the value is a float with two decimal places."""
    try:
        return f"{float(value):.2f}"
    except (ValueError, TypeError):
        return "0.00"

@register.filter
def format_date(date_str):
    # Parse the input string into a datetime object
    dt = datetime.strptime(date_str, "%Y%m%d-%H%M%S")
    # Format the datetime object into a readable string
    return dt.strftime("%d-%m-%Y (%H:%M:%S)")
