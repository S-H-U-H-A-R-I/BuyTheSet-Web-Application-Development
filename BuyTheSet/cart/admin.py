from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.utils import timezone
from datetime import timedelta
from .models import Cart, CartItem


class GuestCartFilter(admin.SimpleListFilter):
    title = 'guest carts'
    parameter_name = 'guest_carts'
    
    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )
        
    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(user=None)
        elif self.value() == 'no':
            return queryset.exclude(user=None)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ['product', 'quantity', 'created_at']
    readonly_fields = ['product', 'created_at']


def delete_old_guest_carts(modeladmin, request, queryset):
    one_day_ago = timezone.now() - timedelta(days=1)
    old_guest_carts = queryset.filter(user=None, created_at__lte=one_day_ago)
    cart_count = old_guest_carts.count()
    old_guest_carts.delete()
    modeladmin.message_user(request, f"Deleted {cart_count} old guest carts.")
delete_old_guest_carts.short_description = "Delete selected old guest carts"
    

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_items', 'created_at')
    list_filter = ('user','created_at', GuestCartFilter)
    actions = [delete_old_guest_carts]
    inlines = [CartItemInline]
    search_fields = ['user__username']
    
    def get_total_items(self, obj):
        return obj.cartitem_set.count()
    get_total_items.short_description = "Total Items"
    
    def created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at.admin_order_field = "created_at"
    created_at.short_description = "Created At"
    
    def is_old_guest_cart(self, obj):
        one_day_ago = timezone.now() - timedelta(days=1)
        return obj.user is None and obj.created_at < one_day_ago
    is_old_guest_cart.boolean = True
    is_old_guest_cart.short_description = "Old Guest Cart"
    
admin.site.register(Cart, CartAdmin)