from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
from store.models import Product


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, validators=[RegexValidator(r'^(?:\+27\d{9}|0\d{9})$', message="Phone number must be entered in the format: '+27123456789' or '0123456789'.")])
    
    class Meta:
        verbose_name = 'Shipping Address'
        verbose_name_plural = 'Shipping Addresses'
        
    def __str__(self):
        return f"Shipping Address for {self.user.username if self.user else 'Guest'}"


# Order model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    shipping_address = models.TextField(max_length=15000, blank=True, null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    is_collect = models.BooleanField(default=False, verbose_name="Collect")
    date_ordered = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=[('paystack', 'Paystack'), ('cash', 'cash')], default='paystack')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_delivered = models.BooleanField(default=False)
    delivered_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Order {self.id}"
    
    def save(self, *args, **kwargs):
        if self.is_collect:
            self.shipping_fee = 0.00
        if self.is_delivered and self.delivered_date is None:
            self.delivered_date = timezone.now()
        super().save(*args, **kwargs)
    
    
# OrderItem model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"