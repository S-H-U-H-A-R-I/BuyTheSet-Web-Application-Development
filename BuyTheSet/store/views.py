import json
from icecream import ic
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q, Value as V
from django.db.models.functions import Replace
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from payments.models import Order
from .forms import SignUpForm, UpdateUserform, ChangePasswordForm, UserInfoForm
from .models import Product, Tag, Profile, ProductImage
from . import services

def register_user(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body.decode('utf-8'))
                form = SignUpForm(data)
                if form.is_valid():
                    ic(form)
                    user = form.save()
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password1']
                    services.link_shipping_addresses(email, user)
                    services.link_orders(email, user)
                    # login user
                    user = authenticate(username=user.username, password=password)
                    login(request, user)
                    return JsonResponse({'redirect': '/'}, status=201)
                else:
                    ic(form.errors)
                    return JsonResponse({'errors': form.errors}, status=400)
            except json.JSONDecodeError:
                return JsonResponse({'error': "Invalid JSON format"}, status=400)
        else:
            return JsonResponse({'error': "Invalid content type"}, status=400)
    else:  
        form = SignUpForm()    
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        password = data['password']
        ic(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'redirect': '/'}, status=200)            
        else:
            ic("authentication failed")
            return JsonResponse({'error': "Invalid username or password"}, status=400)
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'login.html')


def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_user)
        if request.method == 'POST':
            return services.update_user_info(form, request)
        else:
            return render(request, 'update_info.html', {'form': form})
    else:
        messages.error(request, "You are not logged in.", "danger")
        return redirect('login')
            

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            return services.update_user_password(form, request, current_user)
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form': form})       
    else:
        return redirect('login')        


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        if request.method == 'POST':
            user_form = UpdateUserform(request.POST or None, instance=current_user)
            return services.update_user_account(user_form, request, current_user)
        else:
            user_form = UpdateUserform(instance=current_user)
            return render(request, "update_user.html", {'user_form': user_form})
    else:
        return redirect('login')
    
    
def order_history(request):
    if not request.user.is_authenticated:
        return redirect('home')
    orders = Order.objects.filter(user=request.user).order_by("-date_ordered")
    context = {
        "orders": orders
    }
    return render(request, "order_history.html", context)


def order_details(request, order_id):
    if not request.user.is_authenticated:
        return redirect('home')
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        "order": order,
    }
    return render(request, "order_details.html", context)


@csrf_exempt
def update_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('order_id')
        shipping_address = data.get('shipping_address')
        result = services.update_order(order_id, shipping_address)
        return JsonResponse(result)
    return JsonResponse({'success': False})
    

def product(request, pk):
    product = get_object_or_404(Product, id=pk)
    additional_images = ProductImage.objects.filter(product=product)
    images  = [product.image.url] + [f"{settings.MEDIA_URL}{image}" for image in additional_images.values_list('image', flat=True)]
    context = {
        "product": product,
        "images": images,
    }
    return render(request, 'product.html', context)


def home(request):
    tag_name = request.GET.get('tag', None)
    search_query = request.GET.get('q', None)
    message = request.session.pop('message', None)
    alert_type = request.session.pop('alert_type', None)
    tags = Tag.objects.all()
    products = services.get_products_by_tag(tag_name)
    products = services.search_products(products, search_query)
    products = products.filter(is_archived=False).order_by("-is_sale")
    context = {
        'products': products,
        'tags': tags,
        'selected_tag': tag_name,
        'search_query': search_query,
        'message': message,
        'alert_type': alert_type
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def logout_user(request):
    logout(request)
    return redirect('home')

