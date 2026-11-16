from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/register/", views.register_view, name="register"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("products/", views.product_list, name="products"),
    path("products/add/", views.product_create, name="product_add"),
    path("products/<int:pk>/edit/", views.product_edit, name="product_edit"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),
    path("categories/", views.category_list, name="categories"),
    path("categories/add/", views.category_create, name="category_add"),
    path("categories/<int:pk>/edit/", views.category_edit, name="category_edit"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
    path("customers/", views.customer_list, name="customers"),
    path("customers/add/", views.customer_create, name="customer_add"),
    path("customers/<int:pk>/edit/", views.customer_edit, name="customer_edit"),
    path("customers/<int:pk>/delete/", views.customer_delete, name="customer_delete"),
    path("inventory/", views.inventory_view, name="inventory"),
    path("orders/", views.order_list, name="orders"),
    path("orders/add/", views.order_create, name="order_add"),
    path("reports/", views.reports, name="reports"),
]
