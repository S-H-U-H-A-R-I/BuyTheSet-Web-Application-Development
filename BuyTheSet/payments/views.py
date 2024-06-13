import html
import json
from decimal import Decimal
from icecream import ic
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from store.models import Product
from services.cart import GlobalCartService
from .forms import ShippingAddressForm
from .models import ShippingAddress, Order, OrderItem
from . import services
from .utils import is_within_distance, get_cart_items_data
from BuyTheSet.secrets import MAPSJAVASCRIPT_API_KEY
        
        
def checkout(request):
    user = request.user
    cart = GlobalCartService.get_user_cart(request)
    if GlobalCartService.get_total_cart_items(cart) == 0:
        return redirect('home')
    initial_data = {}
    shipping_address = None
    if user.is_authenticated:
        shipping_address = services.get_user_shipping_address(user)
        if shipping_address:
            initial_data = services.get_initial_data_from_shipping_address(shipping_address)
        else:
            initial_data = services.get_initial_data_from_user_profile(user)
    else:
        guest_shipping_address_id = request.session.get('guest_shipping_address_id')
        if guest_shipping_address_id:
            shipping_address = ShippingAddress.objects.get(id=guest_shipping_address_id)
            initial_data = services.get_initial_data_from_shipping_address(shipping_address)
    form = ShippingAddressForm(instance=shipping_address, initial=initial_data)
    cart_items_data = get_cart_items_data(cart)
    cart_total = GlobalCartService.calculate_total_cost_of_cart(cart)
    paystack_public_key = settings.PAYSTACK_PUBLIC_KEY
    default_shipping_fee = Order._meta.get_field('shipping_fee').default
    context = {
        'form': form,
        'cart_items_data': cart_items_data,
        'cart_total': cart_total,
        'paystack_public_key': paystack_public_key,
        'default_shipping_fee': default_shipping_fee,
        'maps_javascript_api_key': MAPSJAVASCRIPT_API_KEY,
    }
    return render(request, 'checkout.html', context)    

    
def save_shipping_info(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            is_collect = request.POST.get('is_collect') == 'True'
            result = services.save_shipping_address(form, request.user, request, is_collect)
            if result['success']:
                return JsonResponse({'success': True})
            else:
                return JsonResponse(result)
        else:
            errors = {field: error[0] for field, error in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request'})
        
    

def check_product_availability(request):
    if request.method == 'POST':
        products_data = json.loads(request.POST.get('products'))
        for product_data in products_data:
            product_name = html.unescape(product_data['name'])
            quantity = product_data['quantity']
            product = get_object_or_404(Product, name=product_name)
            if product.quantity < quantity:
                return JsonResponse({'success': False, 'error': f'Insufficient quantity for product: {product_name}'})
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@csrf_exempt
def save_order(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        products_data = json.loads(request.POST.get('products'))
        amount = request.POST.get('amount')
        shipping_address = request.POST.get('shipping_address', '')
        is_collect = request.POST.get('is_collect') == 'true'
        ic("Testing")
        if is_collect or is_within_distance(shipping_address):
            with transaction.atomic():
                # Create a new Order instance
                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    full_name=f'{first_name} {last_name}',
                    email=email,
                    shipping_address='' if is_collect else shipping_address,
                    amount_paid=Decimal(amount) if payment_method == 'paystack' else Decimal(0),
                    is_collect=is_collect,
                    payment_method=payment_method,
                    total_amount=Decimal(amount),
                )
                ic("Saving order", order)
                order.save()
                # Create OrderItem instances for each purchased product
                for product_data in products_data:
                    product_name = html.unescape(product_data['name'])
                    quantity = product_data['quantity']
                    price = product_data['price']
                    total = product_data['total']
                    # Retrieve the corresponding Product instance based on the product name
                    product = get_object_or_404(Product, name=product_name)
                    if product.quantity >= quantity:
                        product.quantity -= quantity
                        product.save()
                    else:
                        return JsonResponse({'success': False, 'errors': 'Insufficient quantity for product.'})
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=price,
                        user=request.user if request.user.is_authenticated else None,
                    )
                cart = GlobalCartService.get_user_cart(request)
                cart.delete()
                # Send email to the customer if the payment method is 'cash'
                if payment_method == 'cash':
                    subject = 'Order Confirmation'
                    from_email = settings.EMAIL_HOST_USER
                    recipient_list = [order.email, from_email]
                    message = render_to_string('order_confirmation_email.html', {
                        'order': order,
                        'order_items': OrderItem.objects.filter(order=order),
                    })
                    send_mail(subject, message, from_email, recipient_list, html_message=message)
            return JsonResponse({'success': True})
        else:
            errors = {'address1': 'Address is too far from the store.'}
            return JsonResponse({'success': False, 'errors': errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request'})


def payment_success(request):
    return render(request, 'payment_success.html')

