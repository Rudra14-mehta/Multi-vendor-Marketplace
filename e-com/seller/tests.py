from django.shortcuts import render
from django.http import HttpResponseRedirect
import json
import hashlib
from core.models import countryCode, Product, Orders
from .models import Seller
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_sameorigin
from mysite import settings
import uuid
from .forms import ProductForm


# -------------------------------------------------------------------------------------------------------------------------

# --- Store data in sessoin ---
def get_seller_from_session(request):
    try:
        seller = Seller.objects.get(sessionID = request.COOKIES[settings.SELLER_SESSION_COOKIE_NAME])
        if seller is not None:
            return seller
    except:
        return None


def loggedin(request, seller_id):
    
    response = HttpResponseRedirect("../seller")
    
    custom_session_id = uuid.uuid4()
    response.set_cookie(settings.SELLER_SESSION_COOKIE_NAME, custom_session_id)

    seller = Seller.objects.get(id = seller_id)
    seller.sessionID = custom_session_id
    seller.save()

    return response


def authenticate(request, email, password):
    try:
        seller = Seller.objects.get(email = email, password = password)
        if seller is not None:
            return seller.id
        return None
    except Seller.DoesNotExist:
        return None


# # Logic functions

# def insert():
#     with open('/workspaces/Document_Updater/djangotrial/seller/countryCode.json', "r+") as file:
#         data = json.load(file)
#         for val in data:
#             country = val["name"]
#             dialCodes = val["dialCodes"]
#             image = val["image"]
#             if len(dialCodes) > 1:
#                 for dialCode in dialCodes:
#                     sReg = countryCode(country = country, dialCode = dialCode,image = image)
#                     sReg.save()
#                     print(f"country = {country}, dialCode = {dialCode},image = {image}")
#                 print("--- More than 1 dialCode ---")
#             else:
#                 sReg = countryCode(country = country, dialCode = dialCodes[0],image = image)
#                 sReg.save()
#                 print(f"country = {country},\ndialCode = {dialCodes[0]},\nimage = {image}\n\n")
#     return 0

# -------------------------------------------------------------------------------------------------------------------------


# --- Create your views here --- 

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        seller_id = authenticate(request, email, password)

        if seller_id is not None:
            response = loggedin(request, seller_id)
            return response
        else:
            return render(request, "Slogin.html", {"message": f"Worng email or password"})
    else:
                # TO CHANGE SELLER PASSWORD EXPLICITLY
                # seller = Seller.objects.get(email = "dhairya@gmail.com")
                # seller.password = 123
                # seller.save()
        return render(request, "Slogin.html")


def register(request):
    countryCodes = countryCode.objects.all().values()
    first = countryCodes[0]
    if request.method == "POST":

        
        # password = password.encode()
        # password = hashlib.sha256(password)

        seller = {
            "name" : request.POST["name"],
            "email" : request.POST["email"],
            "dialCode" : request.POST["dialCode"],
            "contact" : request.POST["contact"],
            "password" : request.POST["password"],
        }
        request.session["seller"] = seller
        print(f"=== {request.session["seller"]} ===")
        if request.session["seller"] is not None:
            return HttpResponseRedirect("gstin")
        # print(type(dialCode))
        # print(type(contact))

        # country = countryCode[1]
        # print(f"-- REQUESTED \"POST\"{} METHOD --")
        # register = Seller(username = user["name"], email = user["email"], password = user["password"], contact = user["contact"])
        # register.save()
        # return render(request, "dashboard.html", {"name": name})
        return render(request, "Sregister.html")
    else:
        print("GET")
    return render(request, "Sregister.html", {'countryCodes': countryCodes, 'first': first})


def gstin(request):
    print(f" --- {request.session.get("seller")} --- ")
    if request.method == "POST":

        seller_data = request.session.get("seller")
        print(f" --- {seller_data} --- ")

        if seller_data is not None:
            seller = Seller()
            
            fields = [
                # "name",
                # "email",
                # "dialCode",
                # "contact",
                # "password",
                "address",
                "city",
                "district",
                "state",
                "pincode",
                "companyName",
                "gstin",
                "storeName",
            ]

            # FOR DATA FROM PREVIOUS FIELD
            for data in seller_data:
                # print(f"Data: {data}")
                setattr(seller, data, seller_data[data])
                #        ^obj  , ^attr, ^value
                # "setattr" sets value="seller_data[data]" in attribute="data" of object="seller" 
                # For Example:
                #       seller.[element from the list seller_data (i.e. name, email, contact...)] = seller_data[data]
            del request.session["seller"]
            # FOR NEWLY INPUT DATA
            for field in fields:
                setattr(seller,field,request.POST[field])

            # seller = Seller(
            #     name = seller_data["name"],
            #     email = seller_data["email"],
            #     dialCode = seller_data["dialCode"],
            #     contact = seller_data["contact"],
            #     password = seller_data["password"],
            #     address = request.POST["address"],
            #     city = request.POST["city"],
            #     district = request.POST["district"],
            #     state = request.POST["state"],
            #     pincode = request.POST["pincode"],
            #     companyName = request.POST["companyName"],
            #     gstin = request.POST["gstin"],
            #     storeName = request.POST["storeName"],
            # )
            seller.save()
            return HttpResponseRedirect("../seller/login")
        else:
            return HttpResponseRedirect("register")
    else:
        seller_data = request.session.get("seller")
        if seller_data is not None:
            return render(request, "gstin.html")
        else:
            return HttpResponseRedirect("seller")
            return HttpResponseRedirect("register")
        

def main(request):
    print(f"\n>>> {get_seller_from_session(request)}\n")
    seller = get_seller_from_session(request)
    # print(f"\n --- seller : {seller}")
    if seller is not None:
        return render(request, "main.html", {"seller" : seller})
    # else:
    return HttpResponseRedirect("login", {"message": "Something went Worng While Loading"})


def logout(request):
    
    response = HttpResponseRedirect("login")   # using redirect instead of httpresonpse because
    request.session.flush()
    
    response.delete_cookie(settings.SELLER_SESSION_COOKIE_NAME)

    # delete all cookies
    # for cookie in request.COOKIES:
    #     response.delete_cookie(cookie)

    print(f"Cookie Data --->{request.COOKIES}")
    return response


# def deleteAccount(request):
#     seller = get_seller_from_session(request)
#     print(f"--- Seller({seller.name}) Deleted ---")
#     seller.delete()
#     request.session.flush()
#     return HttpResponseRedirect("../")


# --- DASHBOARD ---
@xframe_options_sameorigin
def sidebar(request):
    return render(request, "dashboard/sidebar.html")

@xframe_options_sameorigin
def dashboard(request):
    seller = get_seller_from_session(request)
    seller_products = Product.objects.filter(seller = seller)
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()  # Saves to the database
        # print(f"\n---{product}---")
        # print(f"\n---{product.seller}---")
        return HttpResponseRedirect("dashboard") 
    return render(request, "dashboard/dashboard.html", {"products": seller_products, "choices": Product.categories})

@xframe_options_sameorigin
def products(request):
    seller = get_seller_from_session(request)
    seller_products = Product.objects.filter(seller = seller)
    context = {
        "products": seller_products,
        "categories": Product.CATEGORY_CHOICES,
    }
    if request.method == "POST":
        # currProduct = Product.objects.get(id = request.POST['edit'])
        
        # Instance is passed because it is for updating values of product
        form = ProductForm(request.POST)
        if "edit" in form.data:
            form.instance = form.data['edit']

        # if delete from is submitted
        if "delete" in form.data:
            product = Product.objects.get(id = form.data['delete'])
            product.delete()
            return HttpResponseRedirect("products")
        

        # this is to explicitly pass seller to forms 
        product = form.save(commit=False)
        product.seller = seller

        # validate and save product instance
        if form.is_valid():
            form.save()  # Saves to the database
        else:
            print(form.errors)
        
        # print(f"\n---{product}---")
        # print(f"\n---{product.seller}---")
        return HttpResponseRedirect("products") 
    # To remove delete product
    # d = Product.objects.get(id = 1)
    # d.delete()
    return render(request, "dashboard/products.html", context=context)

@xframe_options_sameorigin
def orders(request):
    return render(request, "dashboard/orders.html")

@xframe_options_sameorigin
def customers(request):
    return render(request, "dashboard/customers.html")

@xframe_options_sameorigin
def profile(request):
    seller = get_seller_from_session(request)
    if seller is not None:
        # print(f"\nSession : {request.session.items()}")
        countryCodes = countryCode.objects.all().values()
        seller_dialCode = countryCode.objects.get(dialCode = seller.dialCode)
        if request.method == "POST":
            try:
                if "Profile" in request.POST:
                    form_data = request.POST
                    
                    fields = [
                        "name",
                        "email",
                        "dialCode",
                        "contact",
                        "password",
                        "address",
                        "city",
                        "district",
                        "state",
                        "pincode",
                        "companyName",
                        "gstin",
                        "storeName",
                    ]
                    
                    for field in fields:
                        if field == "password":
                            if form_data[field] == "":
                                continue
                        # print(f"{field} = {form_data[field]}")
                        # print(f"Field: \'{field}\' \nData: \'{form_data.get(field)}\'")
                        setattr(seller, field, form_data.get(field))

                    # seller.name = form_data["name"]
                    # seller.email = form_data["email"]
                    # seller.dialCode = form_data["dialCode"]
                    # seller.contact = form_data["contact"]
                    # seller.password = form_data["password"]
                    # seller.address = form_data["address"]
                    # seller.city = form_data["city"]
                    # seller.district = form_data["district"]
                    # seller.state = form_data["state"]
                    # seller.pincode = form_data["pincode"]
                    # seller.companyName = form_data["companyName"]
                    # seller.gstin = form_data["gstin"]
                    # seller.storeName = form_data["storeName"]

                    seller.save()
                    
                    return HttpResponseRedirect("../seller/profile")
                
                elif "deleteAccount" in request.POST:
                    print(f"--- DELETE ACCOUNT FORM POST ---")
                    password = request.POST.get("password", "")
                    if password == seller.password:  # Check if entered password matches seller's password
                        
                        # THIS ENSURES THAT MAIN PARENT PAGE ALSO RELOADS ("window.parent.location.reload();")
                        response = HttpResponse("""
                            <html>
                            <body>
                                <script type="text/javascript">
                                    window.parent.location.reload();
                                </script>
                            </body>
                            </html>
                        """)

                        # clears the session
                        request.session.flush()    
                        
                        # delete specific cookies
                        response.delete_cookie(settings.SELLER_SESSION_COOKIE_NAME)

                        # delete all cookies
                        # for cookie in request.COOKIES:
                        #     response.delete_cookie(cookie)
                            
                        print(f"Cookie Data --->{request.COOKIES}")

                        # Uncomment the next line if you want to actually delete the seller
                        # seller.delete()  # Uncomment this line to delete the seller
                        return response    
                    else:
                        # If the passwords don't match, return an error message
                        return render(request, "profile.html", {"seller": seller, "message": "Password didn't match!!"})

            except Exception as e:
                e = str(e)
                error_field = e.split('.')[-1]
                print(f"Exception: {str(e)}")
                context = {
                    "seller_dialCode" : seller_dialCode,
                    "countryCodes": countryCodes,
                    "seller": seller,
                    "error": "Something went Wrong",
                }
                
                context["error"] = f"{error_field.upper()} already exist"
                return render(request, "dashboard/profile.html", context)
                # if "email" in e:
                    
            # print(f"-- POST data: {request.POST} --")
            # return render(request, "dashboard/profile.html", {"seller": seller})
        return render(request, "dashboard/profile.html", {"seller_dialCode" : seller_dialCode, "countryCodes": countryCodes, "seller": seller})
    return HttpResponseRedirect("../seller/login")


# ________________________________________________________________________________________________________________________________________________________________________

from django.shortcuts import render
from django.http import HttpResponseRedirect
import json
import hashlib
from core.models import countryCode, Product, Orders
from .models import Seller
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_sameorigin
from mysite import settings
import uuid
from .forms import ProductForm


# -------------------------------------------------------------------------------------------------------------------------

# --- Store data in sessoin ---
def get_seller_from_session(request):
    try:
        seller = Seller.objects.get(sessionID = request.COOKIES[settings.SELLER_SESSION_COOKIE_NAME])
        if seller is not None:
            return seller
    except:
        return None


def loggedin(request, seller_id):
    
    response = HttpResponseRedirect("../seller")
    
    custom_session_id = uuid.uuid4()
    response.set_cookie(settings.SELLER_SESSION_COOKIE_NAME, custom_session_id)

    seller = Seller.objects.get(id = seller_id)
    seller.sessionID = custom_session_id
    seller.save()

    return response


def authenticate(request, email, password):
    try:
        seller = Seller.objects.get(email = email, password = password)
        if seller is not None:
            return seller.id
        return None
    except Seller.DoesNotExist:
        return None


# # Logic functions

# def insert():
#     with open('/workspaces/Document_Updater/djangotrial/seller/countryCode.json', "r+") as file:
#         data = json.load(file)
#         for val in data:
#             country = val["name"]
#             dialCodes = val["dialCodes"]
#             image = val["image"]
#             if len(dialCodes) > 1:
#                 for dialCode in dialCodes:
#                     sReg = countryCode(country = country, dialCode = dialCode,image = image)
#                     sReg.save()
#                     print(f"country = {country}, dialCode = {dialCode},image = {image}")
#                 print("--- More than 1 dialCode ---")
#             else:
#                 sReg = countryCode(country = country, dialCode = dialCodes[0],image = image)
#                 sReg.save()
#                 print(f"country = {country},\ndialCode = {dialCodes[0]},\nimage = {image}\n\n")
#     return 0

# -------------------------------------------------------------------------------------------------------------------------


# --- Create your views here --- 

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        seller_id = authenticate(request, email, password)

        if seller_id is not None:
            response = loggedin(request, seller_id)
            return response
        else:
            return render(request, "Slogin.html", {"message": f"Worng email or password"})
    else:
                # TO CHANGE SELLER PASSWORD EXPLICITLY
                # seller = Seller.objects.get(email = "dhairya@gmail.com")
                # seller.password = 123
                # seller.save()
        return render(request, "Slogin.html")


def register(request):
    countryCodes = countryCode.objects.all().values()
    first = countryCodes[0]
    if request.method == "POST":

        
        # password = password.encode()
        # password = hashlib.sha256(password)

        seller = {
            "name" : request.POST["name"],
            "email" : request.POST["email"],
            "dialCode" : request.POST["dialCode"],
            "contact" : request.POST["contact"],
            "password" : request.POST["password"],
        }
        request.session["seller"] = seller
        print(f"=== {request.session["seller"]} ===")
        if request.session["seller"] is not None:
            return HttpResponseRedirect("gstin")
        # print(type(dialCode))
        # print(type(contact))

        # country = countryCode[1]
        # print(f"-- REQUESTED \"POST\"{} METHOD --")
        # register = Seller(username = user["name"], email = user["email"], password = user["password"], contact = user["contact"])
        # register.save()
        # return render(request, "dashboard.html", {"name": name})
        return render(request, "Sregister.html")
    else:
        print("GET")
    return render(request, "Sregister.html", {'countryCodes': countryCodes, 'first': first})


def gstin(request):
    print(f" --- {request.session.get("seller")} --- ")
    if request.method == "POST":

        seller_data = request.session.get("seller")
        print(f" --- {seller_data} --- ")

        if seller_data is not None:
            seller = Seller()
            
            fields = [
                # "name",
                # "email",
                # "dialCode",
                # "contact",
                # "password",
                "address",
                "city",
                "district",
                "state",
                "pincode",
                "companyName",
                "gstin",
                "storeName",
            ]

            # FOR DATA FROM PREVIOUS FIELD
            for data in seller_data:
                # print(f"Data: {data}")
                setattr(seller, data, seller_data[data])
                #        ^obj  , ^attr, ^value
                # "setattr" sets value="seller_data[data]" in attribute="data" of object="seller" 
                # For Example:
                #       seller.[element from the list seller_data (i.e. name, email, contact...)] = seller_data[data]
            del request.session["seller"]
            # FOR NEWLY INPUT DATA
            for field in fields:
                setattr(seller,field,request.POST[field])

            # seller = Seller(
            #     name = seller_data["name"],
            #     email = seller_data["email"],
            #     dialCode = seller_data["dialCode"],
            #     contact = seller_data["contact"],
            #     password = seller_data["password"],
            #     address = request.POST["address"],
            #     city = request.POST["city"],
            #     district = request.POST["district"],
            #     state = request.POST["state"],
            #     pincode = request.POST["pincode"],
            #     companyName = request.POST["companyName"],
            #     gstin = request.POST["gstin"],
            #     storeName = request.POST["storeName"],
            # )
            seller.save()
            return HttpResponseRedirect("../seller/login")
        else:
            return HttpResponseRedirect("register")
    else:
        seller_data = request.session.get("seller")
        if seller_data is not None:
            return render(request, "gstin.html")
        else:
            return HttpResponseRedirect("seller")
            return HttpResponseRedirect("register")
        

def main(request):
    print(f"\n>>> {get_seller_from_session(request)}\n")
    seller = get_seller_from_session(request)
    # print(f"\n --- seller : {seller}")
    if seller is not None:
        return render(request, "main.html", {"seller" : seller})
    # else:
    return HttpResponseRedirect("login", {"message": "Something went Worng While Loading"})


def logout(request):
    
    response = HttpResponseRedirect("login")   # using redirect instead of httpresonpse because
    request.session.flush()
    
    response.delete_cookie(settings.SELLER_SESSION_COOKIE_NAME)

    # delete all cookies
    # for cookie in request.COOKIES:
    #     response.delete_cookie(cookie)

    print(f"Cookie Data --->{request.COOKIES}")
    return response


# def deleteAccount(request):
#     seller = get_seller_from_session(request)
#     print(f"--- Seller({seller.name}) Deleted ---")
#     seller.delete()
#     request.session.flush()
#     return HttpResponseRedirect("../")


# --- DASHBOARD ---
@xframe_options_sameorigin
def sidebar(request):
    return render(request, "dashboard/sidebar.html")

@xframe_options_sameorigin
def dashboard(request):
    seller = get_seller_from_session(request)
    seller_products = Product.objects.filter(seller = seller)
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()  # Saves to the database
        # print(f"\n---{product}---")
        # print(f"\n---{product.seller}---")
        return HttpResponseRedirect("dashboard") 
    return render(request, "dashboard/dashboard.html", {"products": seller_products, "choices": Product.categories})

@xframe_options_sameorigin
def products(request):
    seller = get_seller_from_session(request)
    seller_products = Product.objects.filter(seller = seller)
    if request.method == "POST":
        currProduct = Product.objects.get(id = request.POST['edit'])
        # Instance is passed because it is for edit
        form = ProductForm(request.POST)
        if "edit" in form.data:
            form.instance = currProduct
            # this is to explicitly pass seller to forms 
            product = form.save(commit=False)
            product.seller = seller

            # validate and save product instance
            if form.is_valid():
                print(product.seller)
                form.save()  # Saves to the database
            else:
                print(form.errors)
        # print(f"\n---{product}---")
        # print(f"\n---{product.seller}---")
        return HttpResponseRedirect("products") 
    # To remove delete product
    # d = Product.objects.get(id = 1)
    # d.delete()
    return render(request, "dashboard/products.html", {"products": seller_products, "categories": Product.CATEGORY_CHOICES})

@xframe_options_sameorigin
def orders(request):
    return render(request, "dashboard/orders.html")

@xframe_options_sameorigin
def customers(request):
    return render(request, "dashboard/customers.html")

@xframe_options_sameorigin
def profile(request):
    seller = get_seller_from_session(request)
    if seller is not None:
        # print(f"\nSession : {request.session.items()}")
        countryCodes = countryCode.objects.all().values()
        seller_dialCode = countryCode.objects.get(dialCode = seller.dialCode)
        if request.method == "POST":
            try:
                if "Profile" in request.POST:
                    form_data = request.POST
                    
                    fields = [
                        "name",
                        "email",
                        "dialCode",
                        "contact",
                        "password",
                        "address",
                        "city",
                        "district",
                        "state",
                        "pincode",
                        "companyName",
                        "gstin",
                        "storeName",
                    ]
                    
                    for field in fields:
                        if field == "password":
                            if form_data[field] == "":
                                continue
                        # print(f"{field} = {form_data[field]}")
                        # print(f"Field: \'{field}\' \nData: \'{form_data.get(field)}\'")
                        setattr(seller, field, form_data.get(field))

                    # seller.name = form_data["name"]
                    # seller.email = form_data["email"]
                    # seller.dialCode = form_data["dialCode"]
                    # seller.contact = form_data["contact"]
                    # seller.password = form_data["password"]
                    # seller.address = form_data["address"]
                    # seller.city = form_data["city"]
                    # seller.district = form_data["district"]
                    # seller.state = form_data["state"]
                    # seller.pincode = form_data["pincode"]
                    # seller.companyName = form_data["companyName"]
                    # seller.gstin = form_data["gstin"]
                    # seller.storeName = form_data["storeName"]

                    seller.save()
                    
                    return HttpResponseRedirect("../seller/profile")
                
                elif "deleteAccount" in request.POST:
                    print(f"--- DELETE ACCOUNT FORM POST ---")
                    password = request.POST.get("password", "")
                    if password == seller.password:  # Check if entered password matches seller's password
                        
                        # THIS ENSURES THAT MAIN PARENT PAGE ALSO RELOADS ("window.parent.location.reload();")
                        response = HttpResponse("""
                            <html>
                            <body>
                                <script type="text/javascript">
                                    window.parent.location.reload();
                                </script>
                            </body>
                            </html>
                        """)

                        # clears the session
                        request.session.flush()    
                        
                        # delete specific cookies
                        response.delete_cookie(settings.SELLER_SESSION_COOKIE_NAME)

                        # delete all cookies
                        # for cookie in request.COOKIES:
                        #     response.delete_cookie(cookie)
                            
                        print(f"Cookie Data --->{request.COOKIES}")

                        # Uncomment the next line if you want to actually delete the seller
                        # seller.delete()  # Uncomment this line to delete the seller
                        return response    
                    else:
                        # If the passwords don't match, return an error message
                        return render(request, "profile.html", {"seller": seller, "message": "Password didn't match!!"})

            except Exception as e:
                e = str(e)
                error_field = e.split('.')[-1]
                print(f"Exception: {str(e)}")
                context = {
                    "seller_dialCode" : seller_dialCode,
                    "countryCodes": countryCodes,
                    "seller": seller,
                    "error": "Something went Wrong",
                }
                
                context["error"] = f"{error_field.upper()} already exist"
                return render(request, "dashboard/profile.html", context)
                # if "email" in e:
                    
            # print(f"-- POST data: {request.POST} --")
            # return render(request, "dashboard/profile.html", {"seller": seller})
        return render(request, "dashboard/profile.html", {"seller_dialCode" : seller_dialCode, "countryCodes": countryCodes, "seller": seller})
    return HttpResponseRedirect("../seller/login")
