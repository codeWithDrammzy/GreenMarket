from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import*

# home
def home(request):
    return render(request, ('greenmarket/homepage/home.html'))

# login
def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)  # ✅ this logs the user in
                return redirect('dashboard')  # ✅ redirects to dashboard
            else:
                form.add_error(None, "Invalid username or password")  # optional user feedback

    context = {'form': form}
    return render(request, 'greenmarket/homepage/my-login.html', context)

# registration 
def registration_page(request):

    form = UserCreationForm()
    if request.method =="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('my-login')
    
    context = {'form': form}

    return render(request, 'greenmarket/homepage/registration-page.html', context)

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
    return render(request, 'greenmarket/farmerpage/product-list.html')

# add product
def add_product(request):
    return render(request, 'greenmarket/farmerpage/add-product.html')


# ============= Buyer views =============
# dashboard
def buyer_dashboard(request):
    return render(request, 'greenmarket/buyerpage/buyer-dashboard.html')
