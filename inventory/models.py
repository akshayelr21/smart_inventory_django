from django.conf import settings
from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    ROLE_CHOICES = [("ADMIN", "Admin"), ("STAFF", "Staff")]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="STAFF")

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    def __str__(self): return self.name

class Product(models.Model):
    name = models.CharField(max_length=160)
    sku = models.CharField(max_length=60, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def is_low_stock(self): return self.quantity <= self.reorder_level
    def __str__(self): return f"{self.name} ({self.sku})"

class Customer(models.Model):
    name = models.CharField(max_length=160)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class StockMovement(models.Model):
    TYPES = [("IN", "Stock In"), ("OUT", "Stock Out")]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="movements")
    movement_type = models.CharField(max_length=3, choices=TYPES)
    quantity = models.PositiveIntegerField()
    note = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.product} - {self.movement_type} {self.quantity}"

class Order(models.Model):
    STATUS = [("PENDING", "Pending"), ("COMPLETED", "Completed"), ("CANCELLED", "Cancelled")]
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    status = models.CharField(max_length=12, choices=STATUS, default="COMPLETED")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self): return f"Order #{self.pk}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    @property
    def line_total(self): return self.quantity * self.unit_price
