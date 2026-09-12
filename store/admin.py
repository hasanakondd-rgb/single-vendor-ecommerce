from django.contrib import admin

from .models import Customer, Order, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "quantity", "featured")
    list_filter = ("category", "featured")
    search_fields = ("name", "description")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone")
    search_fields = ("name", "phone")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "product",
        "quantity",
        "total_price",
        "order_date",
    )
    list_filter = ("order_date",)
