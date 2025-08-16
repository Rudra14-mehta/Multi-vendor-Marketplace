from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("gstin", views.gstin, name="gstin"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("sidebar", views.sidebar, name="sidebar"),
    path("profile", views.profile, name="profile"),
    path("products", views.products, name="products"),
    path("orders", views.orders, name="orders"),
    path("customers", views.customers, name="customers"),
    # path("deleteAccount", views.deleteAccount, name="deleteAccount"),
]
