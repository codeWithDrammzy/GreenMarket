from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import*
from .forms import*

# ===================== Authentication Views =====================

def registration_page(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            user_type = form.cleaned_data['user_type']

            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return render(request, 'greenmarket/homepage/register-page.html', {'form': form})

            if User.objects.filter(username=email).exists():
                messages.error(request, "User with this email already exists.")
                return render(request, 'greenmarket/homepage/register-page.html', {'form': form})

            user = User.objects.create_user(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password1
            )

            if user_type == 'farmer':
                FarmerModel.objects.create(user=user, user_type='farmer')
            elif user_type == 'buyer':
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

            if user is not None:
                login(request, user)

                if user.is_superuser: 
                    return redirect('/admin/')
                elif hasattr(user, 'farmermodel') and user.farmermodel.user_type == "farmer":
                    return redirect('dashboard')
                elif hasattr(user, 'buyermodel') and user.buyermodel.user_type == "buyer":
                    return redirect('buyer-dashboard')
                else:
                    messages.error(request, "User role not recognized.")
                    return redirect('login')
            else:
                messages.error(request, "Invalid login credentials")

    return render(request, 'greenmarket/homepage/login.html', {'form': form})


def my_logout(request):
    logout(request)
    return redirect('home')


# ===================== Home View =====================

def home(request):
    items = Product.objects.all().order_by('-date_added')[:4]
    context = {'items':items}
    return render(request, 'greenmarket/homepage/home.html', context)


# ===================== Farmer Views =====================

@login_required(login_url='login')
def farmers_dashboard(request):
    farmer = request.user.farmermodel   
    farm_items = Product.objects.filter(farmer= farmer).count()
    context = {'farm_items':farm_items}
    return render(request, 'greenmarket/farmerpage/dashboard.html',context)


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
            try:
                farmer = FarmerModel.objects.get(user=request.user)
                product.farmer = farmer  # 🟢 this is the actual foreign key
                product.save()
                return redirect('product-list')
            except FarmerModel.DoesNotExist:
                return HttpResponse("Only farmers can add products.")
    return render(request, 'greenmarket/farmerpage/add-product.html', {'form': form})

@login_required(login_url='login')
def product_info(request, pk):
    product= Product.objects.get(id=pk)
    context = {'product': product}
    return render(request, 'greenmarket/farmerpage/product-info.html', context)

@login_required(login_url='login')
def delete_product(request, pk):
    product =Product.objects.get(id= pk)
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
    context = {'items':items}
    return render(request, 'greenmarket/buyerpage/market-place.html', context)

@login_required(login_url='login')
def my_order(request):
    return render(request, 'greenmarket/buyerpage/my-order.html')
