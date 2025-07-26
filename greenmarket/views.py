from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from decimal import Decimal

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
    farmer = request.user.farmermodel
    my_products = Product.objects.filter(farmer=farmer)

    order_items = OrderItem.objects.filter(product__in=my_products) \
        .select_related('order', 'product', 'order__buyer__user') \
        .order_by('-order__order_date')

    context = {
        'order_items': order_items
    }
    return render(request, 'greenmarket/farmerpage/farm-order.html', context)


@login_required(login_url='login')
def check_in(request, pk):
    order = get_object_or_404(Order, pk=pk)
    farmer = request.user.farmermodel
    my_products = Product.objects.filter(farmer=farmer)

    order_items = OrderItem.objects.filter(order=order, product__in=my_products) \
    .select_related('product', 'order', 'order__buyer')
    context = {
        'order': order,
        'order_items': order_items 
    }

    return render(request, 'greenmarket/farmerpage/check-in.html', context)


# ===================== Buyer Views =====================

@login_required(login_url='login')
def buyer_dashboard(request):
    buyer = request.user.buyermodel
    orders = Order.objects.filter(buyer=buyer)
    order_count = orders.count()
    pending_orders = Order.objects.filter(status = 'pending').count()
    recent_orders = Order.objects.filter(buyer=buyer).order_by('-order_date')[:3]
    context = {
        'orders': orders,
        'order_count': order_count,
        'pending_orders':pending_orders,
        'recent_orders':recent_orders
    }
    return render(request, 'greenmarket/buyerpage/buyer-dashboard.html', context)



@login_required(login_url='login')
def market_place(request):
    items = Product.objects.all().order_by('-date_added')
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    return render(request, 'greenmarket/buyerpage/market-place.html', {
        'items': items,
        'cart_count': cart_count
    })


from django.utils.timezone import localtime

@login_required(login_url='login')
def my_order(request):
    buyer = request.user.buyermodel
    orders = Order.objects.filter(buyer=buyer).order_by('-order_date')
    context ={'orders': orders}
    return render(request, 'greenmarket/buyerpage/my-order.html', context)



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


from django.db import transaction

@login_required(login_url='login')
def send_order_request(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect('check-out')

        buyer = request.user.buyermodel
        products = Product.objects.filter(id__in=cart.keys())

        with transaction.atomic():
            order = Order.objects.create(buyer=buyer, status='pending')  # 🟢 PENDING for approval

            total = 0
            for product in products:
                quantity = cart[str(product.id)]
                price = product.price
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                total += quantity * price

            order.total_amount = total
            order.save()

            # Optional: Clear cart after sending request
            request.session['cart'] = {}
            request.session.modified = True

        messages.success(request, "Your request has been sent to the farmer(s).")
        return redirect('my-order')

    return redirect('check-out')

















# this is to clear the cart (asuming the payment is completed)
@login_required(login_url='login')
def confirm_payment(request):
    cart = request.session.get('cart', {})
    
    # Fetch buyer model
    try:
        buyer = request.user.buyermodel
    except BuyerModel.DoesNotExist:
        messages.error(request, "Only buyers can place an order.")
        return redirect('home')

    # Fetch product info
    products = Product.objects.filter(id__in=cart.keys())
    if not products.exists():
        messages.error(request, "Cart contains invalid items.")
        return redirect('check-out')

    # Create the order
    order = Order.objects.create(
        buyer=buyer,
        order_date=timezone.now(),
        total_amount=0.00,  # Will be updated below
        is_paid=False
    )

    total = Decimal("0.00")

    for product in products:
        quantity = cart[str(product.id)]
        total_price = quantity * product.price
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )
        total += total_price

    # Update the total amount
    order.total_amount = total
    order.save()

    # Clear the cart
    request.session['cart'] = {}
    request.session.modified = True

    messages.success(request, "Payment confirmed. Order placed successfully.")
    return redirect('my-order')



