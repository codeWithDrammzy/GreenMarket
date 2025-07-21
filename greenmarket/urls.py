from django.urls import path 
from .import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login', views.my_login, name='login'),  # rename the name

    path('my-logout', views.my_logout, name='my-logout'),
    path('register-page', views.registration_page, name='register-page'),

    # =========== Farmer url===========
    path('dashboard', views.farmers_dashboard, name='dashboard'),
    path('product-list', views.product_list, name='product-list'),
    path('add-product', views.add_product, name='add-product'),

    # ============ Buyer page ===========

    path('buyer-dashboard', views.buyer_dashboard, name='buyer-dashboard')
    

]
