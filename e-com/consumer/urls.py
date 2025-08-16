from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("profile/address", views.address, name="address"),
    path('product/<slug:slug>/<int:pk>/', views.product_detail, name='product_detail'),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("checkout/orderConfirmation", views.orderConfirmation, name="orderConfirmation"),
    path("orders", views.orders, name="orders"),
    path("test", views.test, name="test"),
    path('search/', views.search, name='search'),
    path('cart/count', views.cart_count, name='cart_count'),
]
