from django.contrib import admin
from .models import Products, Category, Order, CustomerOrder,Custom
# Register your models here.

admin.site.register(Products)

admin.site.register(Custom)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(CustomerOrder)



