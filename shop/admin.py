from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.order import Order

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=["name","price","description","category"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=["name"]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=["first_name","last_name","email","contact","password"]

@admin.register(Order)
class OderAdmin(admin.ModelAdmin):
    list_display=["product","customer","quantity","price","address","phone","date","status"]