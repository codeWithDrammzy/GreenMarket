from django.contrib import admin
from .models import FarmerModel, BuyerModel, Product

admin.site.register(FarmerModel)
admin.site.register(BuyerModel)
admin.site.register(Product)
