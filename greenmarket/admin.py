from django.contrib import admin
from .models import*

admin.site.register(FarmerModel)
admin.site.register(BuyerModel)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)


