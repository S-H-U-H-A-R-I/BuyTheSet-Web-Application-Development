from django import forms
from .models import ShippingAddress

class PaymentForm(forms.Form):
    stripeToken = forms.CharField(widget=forms.HiddenInput())
    
# Create a form for the shipping address
class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('full_name', 'email', 'phone_number', 'address1', 'address2')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 1'}),
            'address2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 2 (optional)'}),
        }
        labels = {
            'full_name': '',
            'email': '',
            'phone_number': '',
            'address1': '',
            'address2': '',
        }
        error_messages = {
            'full_name': {
               'required': 'Please enter your full name',
            },
            'email': {
               'required': 'Please enter your email address',
               'invalid': 'Please enter a valid email address',
            },
            'phone_number': {
               'required': 'Please enter your phone number',
               'invalid': 'Please enter a valid phone number in the format: "+27123456789" or "0123456789"',
            },
            'address1': {
               'required': 'Please enter your address',
            },
        }