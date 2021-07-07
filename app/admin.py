from django.contrib import admin
from .models import Product, Profile, Cart, OrderPlaced


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','description', 'category','cutPrice', 'price', 'image']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','name', 'city','state']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'product_id', 'quan']

@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ["user", "profile","product", "quan"]