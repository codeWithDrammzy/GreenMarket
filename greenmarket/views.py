from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import*
from django.contrib.auth.models import User


# home
def home(request):
    return render(request, ('greenmarket/homepage/home.html'))


def my_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Use .filter().first() instead of try/except
            user = User.objects.filter(email=email).first()
            
            if user:
                # Authenticate using the username
                user = authenticate(request, username=user.username, password=password)
                if user:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    form.add_error(None, "Invalid email or password")
            else:
                form.add_error(None, "No account found with that email")

    return render(request, 'greenmarket/homepage/my-login.html', {'form': form})


def registration_page(request):
    form = FarmerRegistrationForm()
    if request.method == "POST":
        form = FarmerRegistrationForm(request.POST)
        if form.is_valid():
            first = form.cleaned_data['first_name']
            last = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['pass1']
            user_type = form.cleaned_data['user_type']  # not used yet, just collected

            # ✅ Manually create the user in Django's User model
            user = User.objects.create_user(
                username=email,
                first_name=first,
                last_name=last,
                email=email,
                password=password
            )

            return redirect('my-login')

    return render(request, 'greenmarket/homepage/registration-page.html', {'form': form})

# logout
def my_logout(request):
    logout(request)
    return redirect(home)


# ================== Farmer views ================
#  dashboard
@login_required(login_url='my-login')
def farmers_dasboard(request):

    return render(request, 'greenmarket/farmerpage/dashboard.html')

# prodict list
def product_list(request):
    products = FarmProduct.objects.all()

    context = {'products':products}
    return render(request, 'greenmarket/farmerpage/product-list.html', context)

# add product
def add_product(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product-list')
    context ={'form':form}
            
    return render(request, 'greenmarket/farmerpage/add-product.html', context)


# ============= Buyer views =============
# dashboard
def buyer_dashboard(request):
    return render(request, 'greenmarket/buyerpage/buyer-dashboard.html')
