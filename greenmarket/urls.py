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
    path('product-info/<int:pk>', views.product_info, name='product-info'),
    path('delete-product/<int:pk>', views.delete_product, name='delete-product'),
    path('farm-orders', views.farm_orders, name='farm-orders'),

    # ============ Buyer page ===========

    path('buyer-dashboard', views.buyer_dashboard, name='buyer-dashboard'),
    path('market-place', views.market_place, name='market-place'),
    path('my-order', views.my_order, name='my-order'),
    

]
