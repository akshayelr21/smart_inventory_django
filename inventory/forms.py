from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Product, Category, Customer, StockMovement

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit: user.save()
        return user

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "sku", "category", "description", "price", "quantity", "reorder_level"]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "email", "phone", "address"]

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ["product", "movement_type", "quantity", "note"]
