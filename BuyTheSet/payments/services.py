import json
import requests
from icecream import ic
from .models import ShippingAddress
from .utils import create_shipping_address
from store.models import Profile


def get_user_shipping_address(user):
    return ShippingAddress.objects.filter(user=user).first()


def get_initial_data_from_shipping_address(shipping_address):
    return {
        'full_name': shipping_address.full_name,
        'email': shipping_address.email,
        'address1': shipping_address.address1,
        'address2': shipping_address.address2,
        'phone_number': shipping_address.phone_number,
    }


def get_initial_data_from_user_profile(user):
    profile = Profile.objects.filter(user=user).first()
    if profile:
        return {
            'full_name': user.get_full_name(),
            'email': profile.email,
            'phone_number': profile.phone_number,
            'address1': profile.address1,
            'address2': profile.address2,
        }
    return {}


def save_shipping_address(form, user, request, is_collect):
    address1 = form.cleaned_data['address1']
    if not is_collect and not address1:
        return {'success': False, 'errors': {'address1': 'Address is required.'}}
    shipping_address = get_user_shipping_address(user)
    if shipping_address:
        # If a shipping address already exists, only update the name, email, and phone number
        shipping_address.full_name = form.cleaned_data['full_name']
        shipping_address.email = form.cleaned_data['email']
        shipping_address.phone_number = form.cleaned_data['phone_number']
        if not is_collect:
            # If the order is not for collection, update the address
            shipping_address.address1 = address1
            shipping_address.address2 = form.cleaned_data['address2']
    else:
        # If no shipping address exists, create a new one
        shipping_address = create_shipping_address(form, user, is_collect)
    shipping_address.save()
    if not user.is_authenticated:
        request.session['guest_shipping_address_id'] = shipping_address.id
    return {'success': True}
