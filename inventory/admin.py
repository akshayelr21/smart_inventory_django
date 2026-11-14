from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, Category, Product, Customer, StockMovement, Order, OrderItem

class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(StockMovement)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status", "total", "created_at")
    inlines = [OrderItemInline]
admin.site.register(Order, OrderAdmin)
