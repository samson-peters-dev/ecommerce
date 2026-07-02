from django.contrib import admin

# Register your models here.
from . models import Category, Product, Cart, CartProduct,Order

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)