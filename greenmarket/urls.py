from django.urls import path 
from .import views

urlpatterns = [
    path('', views.home, name=''),

    path('my-login', views.my_login, name='my-login'),
    path('registration-page', views.registration_page, name='registration-page'),

    # =========== Farmer url===========
    path('dashboard', views.farmers_dasboard, name='dashboard'),
    path('product-list', views.product_list, name='product-list'),
    path('add-product', views.add_product, name='add-product'),

    # ============ Buyer page ===========

    path('buyer-dashboard', views.buyer_dashboard, name='buyer-dashboard')
    

]
