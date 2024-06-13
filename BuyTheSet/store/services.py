from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login
from django.db.models import Q
from django.shortcuts import redirect, render
from payments.models import Order, ShippingAddress
from .models import Tag, Product


def link_shipping_addresses(email, user):
    shipping_addresses = ShippingAddress.objects.filter(email=email)
    if shipping_addresses.exists():
        shipping_addresses.update(user=user)


def link_orders(email, user):
    orders = Order.objects.filter(email=email)
    if orders.exists():
        orders.update(user=user)


def update_user_account(form, request, current_user):
    if form.is_valid():
        form.save()
        login(request, current_user)
        return redirect('home')
    else:
        return render(request, "update_user.html", {'user_form': form})


def update_user_info(form, request):
    if form.is_valid():
        form.save()
        messages.success(request, "Your information has been updated successfully.", "success")
    else:
        for error in list(form.errors.values()):
            messages.error(request, error[0], "danger")
    return redirect('update_info')


def update_user_password(form, request, current_user):
    if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return redirect('home')
    else:
        context = {'form': form}
        return render(request, "update_password.html", context)


def get_products_by_tag(tag_name):
    if tag_name:
        tag = Tag.objects.filter(name=tag_name).first()
        if tag:
            return Product.objects.filter(tag=tag, quantity__gt=0).order_by("-is_sale")    
    return Product.objects.filter(quantity__gt=0).order_by("-is_sale")


def search_products(products, search_query):
    if search_query:
        search_terms = search_query.split()
        query = Q()
        for term in search_terms:
            query |= Q(name__icontains=term) | Q(description__icontains=term) | Q(verbose_name__icontains=term)
        return products.filter(query).order_by("-is_sale").distinct()
    return products


def update_order(order_id, shipping_address):
    try:
        order = Order.objects.get(id=order_id)
        order.shipping_address = shipping_address
        order.save()
        return {'success': True}
    except Order.DoesNotExist:
        return {'success': False}