from django.shortcuts import render

# home
def home(request):
    return render(request, ('greenmarket/homepage/home.html'))

# about
def my_login(request):
    return render(request, ('greenmarket/homepage/my-login.html'))

# registration 

def registration_page(request):
    return render(request, 'greenmarket/homepage/registration-page.html')



# ================== Farmer views ================
#  dashboard
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
