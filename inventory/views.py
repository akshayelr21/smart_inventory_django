from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.db.models import Sum, F
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import RegisterForm, ProductForm, CustomerForm, StockMovementForm
from .models import Product, Category, Customer, Order, OrderItem, StockMovement

def register_view(request):
    if request.user.is_authenticated: return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Staff account created. Please sign in.")
        return redirect("login")
    return render(request, "registration/register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated: return redirect("dashboard")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("dashboard")
    return render(request, "registration/login.html", {"form": form})

@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    context = {
        "product_count": Product.objects.count(),
        "customer_count": Customer.objects.count(),
        "order_count": Order.objects.count(),
        "low_stock": Product.objects.filter(quantity__lte=F("reorder_level")).order_by("quantity")[:6],
        "recent_orders": Order.objects.select_related("customer").order_by("-created_at")[:6],
        "sales_total": Order.objects.exclude(status="CANCELLED").aggregate(total=Sum("total"))["total"] or Decimal("0.00"),
    }
    return render(request, "inventory/dashboard.html", context)

@login_required
def product_list(request):
    q = request.GET.get("q", "")
    products = Product.objects.select_related("category").order_by("name")
    if q: products = products.filter(name__icontains=q) | products.filter(sku__icontains=q)
    return render(request, "inventory/products.html", {"products": products, "q": q})

@login_required
def product_create(request):
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save(); messages.success(request, "Product added."); return redirect("products")
    return render(request, "inventory/form.html", {"form": form, "title": "Add Product"})

@login_required
def product_edit(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save(); messages.success(request, "Product updated."); return redirect("products")
    return render(request, "inventory/form.html", {"form": form, "title": "Edit Product"})

@login_required
def product_delete(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        obj.delete(); messages.success(request, "Product deleted."); return redirect("products")
    return render(request, "inventory/confirm_delete.html", {"object": obj})

@login_required
def customer_list(request):
    q = request.GET.get("q", "")
    customers = Customer.objects.order_by("name")
    if q: customers = customers.filter(name__icontains=q)
    return render(request, "inventory/customers.html", {"customers": customers, "q": q})

@login_required
def customer_create(request):
    form = CustomerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save(); messages.success(request, "Customer added."); return redirect("customers")
    return render(request, "inventory/form.html", {"form": form, "title": "Add Customer"})

@login_required
def customer_edit(request, pk):
    obj = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save(); messages.success(request, "Customer updated."); return redirect("customers")
    return render(request, "inventory/form.html", {"form": form, "title": "Edit Customer"})

@login_required
def customer_delete(request, pk):
    obj = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        obj.delete(); messages.success(request, "Customer deleted."); return redirect("customers")
    return render(request, "inventory/confirm_delete.html", {"object": obj})

@login_required
def inventory_view(request):
    form = StockMovementForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        movement = form.save(commit=False)
        product = movement.product
        if movement.movement_type == "OUT" and product.quantity < movement.quantity:
            form.add_error("quantity", "Not enough stock available.")
        else:
            with transaction.atomic():
                product = Product.objects.select_for_update().get(pk=product.pk)
                if movement.movement_type == "IN": product.quantity += movement.quantity
                else: product.quantity -= movement.quantity
                product.save()
                movement.created_by = request.user
                movement.save()
            messages.success(request, "Stock updated.")
            return redirect("inventory")
    movements = StockMovement.objects.select_related("product", "created_by").order_by("-created_at")[:30]
    low_stock = Product.objects.filter(quantity__lte=F("reorder_level"))
    return render(request, "inventory/stock.html", {"form": form, "movements": movements, "low_stock": low_stock})

@login_required
def order_list(request):
    orders = Order.objects.select_related("customer").order_by("-created_at")
    return render(request, "inventory/orders.html", {"orders": orders})

@login_required
def order_create(request):
    customers = Customer.objects.all().order_by("name")
    products = Product.objects.all().order_by("name")
    if request.method == "POST":
        customer_id = request.POST.get("customer")
        product_id = request.POST.get("product")
        try:
            qty = int(request.POST.get("quantity", "0"))
            product = Product.objects.get(pk=product_id)
            customer = Customer.objects.get(pk=customer_id)
            if qty < 1: raise ValueError()
            with transaction.atomic():
                product = Product.objects.select_for_update().get(pk=product.pk)
                if product.quantity < qty:
                    messages.error(request, "Insufficient stock.")
                else:
                    order = Order.objects.create(customer=customer, created_by=request.user, total=product.price * qty)
                    OrderItem.objects.create(order=order, product=product, quantity=qty, unit_price=product.price)
                    product.quantity -= qty; product.save()
                    StockMovement.objects.create(product=product, movement_type="OUT", quantity=qty, note=f"Order #{order.pk}", created_by=request.user)
                    messages.success(request, f"Order #{order.pk} created.")
                    return redirect("orders")
        except (Product.DoesNotExist, Customer.DoesNotExist, ValueError, TypeError):
            messages.error(request, "Please select a valid customer, product, and quantity.")
    return render(request, "inventory/order_form.html", {"customers": customers, "products": products})

@login_required
def reports(request):
    sales = Order.objects.exclude(status="CANCELLED").aggregate(total=Sum("total"))["total"] or Decimal("0.00")
    return render(request, "inventory/reports.html", {
        "sales": sales,
        "order_count": Order.objects.exclude(status="CANCELLED").count(),
        "stock_value": sum((p.price * p.quantity for p in Product.objects.all()), Decimal("0.00")),
        "low_stock": Product.objects.filter(quantity__lte=F("reorder_level")).count(),
    })
