from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'address1', 'address2')
    search_fields = ('user__username', 'full_name', 'email')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')
    exclude = ('user',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'email', 'amount_paid', 'date_ordered', 'is_collect')
    search_fields = ('user__username', 'full_name', 'email')
    date_hierarchy = 'date_ordered'
    inlines = [OrderItemInline]
    
