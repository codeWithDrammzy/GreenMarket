from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import *
from .forms import *


# ===================== Authentication Views =====================

def registration_page(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['password1'] != data['password2']:
                messages.error(request, "Passwords do not match.")
                return render(request, 'greenmarket/homepage/register-page.html', {'form': form})

            if User.objects.filter(username=data['email']).exists():
                messages.error(request, "User with this email already exists.")
                return render(request, 'greenmarket/homepage/register-page.html', {'form': form})

            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password1']
            )

            if data['user_type'] == 'farmer':
                FarmerModel.objects.create(user=user, user_type='farmer')
            else:
                BuyerModel.objects.create(user=user, user_type='buyer')

            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'greenmarket/homepage/register-page.html', {'form': form})


def my_login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

            if user:
                login(request, user)
                if user.is_superuser:
                    return redirect('/admin/')
                elif hasattr(user, 'farmermodel'):
                    return redirect('dashboard')
                elif hasattr(user, 'buyermodel'):
                    return redirect('buyer-dashboard')
                else:
                    messages.error(request, "User role not recognized.")
            else:
                messages.error(request, "Invalid login credentials")

    return render(request, 'greenmarket/homepage/login.html', {'form': form})


def my_logout(request):
    logout(request)
    return redirect('home')


# ===================== Home View =====================

def home(request):
    items = Product.objects.all().order_by('-date_added')[:4]
    return render(request, 'greenmarket/homepage/home.html', {'items': items})


# ===================== Farmer Views =====================

@login_required(login_url='login')
def farmers_dashboard(request):
    farmer = request.user.farmermodel
    farm_items = Product.objects.filter(farmer=farmer).count()
    return render(request, 'greenmarket/farmerpage/dashboard.html', {'farm_items': farm_items})


@login_required(login_url='login')
def product_list(request):
    products = Product.objects.filter(farmer=request.user.farmermodel)
    return render(request, 'greenmarket/farmerpage/product-list.html', {'products': products})


@login_required(login_url='login')
def add_product(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user.farmermodel
            product.save()
            return redirect('product-list')
    return render(request, 'greenmarket/farmerpage/add-product.html', {'form': form})


@login_required(login_url='login')
def product_info(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'greenmarket/farmerpage/product-info.html', {'product': product})


@login_required(login_url='login')
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    product.delete()
    return redirect('product-list')


@login_required(login_url='login')
def farm_orders(request):
    return render(request, 'greenmarket/farmerpage/farm-order.html')


# ===================== Buyer Views =====================

@login_required(login_url='login')
def buyer_dashboard(request):
    return render(request, 'greenmarket/buyerpage/buyer-dashboard.html')


@login_required(login_url='login')
def market_place(request):
    items = Product.objects.all().order_by('-date_added')
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    return render(request, 'greenmarket/buyerpage/market-place.html', {
        'items': items,
        'cart_count': cart_count
    })


@login_required(login_url='login')
def my_order(request):
    return render(request, 'greenmarket/buyerpage/my-order.html')


@login_required(login_url='login')
def check_out(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    subtotal = 0

    for product in products:
        quantity = cart[str(product.id)]
        total_price = quantity * product.price
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price
        })
        subtotal += total_price  # ✅ fix the subtotal here

    return render(request, 'greenmarket/buyerpage/check-out.html', {
        'cart_items': cart_items,
        'total': subtotal
    })


@login_required(login_url='login')
def buyer_prof(request):
    try:
        profile = request.user.buyermodel
    except BuyerModel.DoesNotExist:
        messages.error(request, "Only buyers can access this page.")
        return redirect('home')

    if request.method == 'POST':
        form = BuyerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('buyer-dashboard')
    else:
        form = BuyerProfileForm(instance=profile)

    return render(request, 'greenmarket/buyerpage/profile.html', {'form': form})


# ===================== Cart Views =====================

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    return redirect('market-place')


# add to the cart with the + sign
def increase_cart_item(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return redirect('check-out')


# substrat from the cart
def decrease_cart_item(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            del cart[product_id]
    request.session['cart'] = cart
    return redirect('check-out')


# this is to clear the cart (asuming the payment is completed)
def confirm_payment(request):
    if request.method == 'POST':
        request.session['cart'] = {}  
        request.session.modified = True  
        return redirect('check-out') 
