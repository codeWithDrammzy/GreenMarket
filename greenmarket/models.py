from django.db import models
from django.contrib.auth.models import User

# ----------------------------
# Farmer Model
# ----------------------------
class FarmerModel(models.Model):
    USER_TYPE_CHOICES = (
        ('farmer', 'Farmer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='farmer')
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# ----------------------------
# Buyer Model
# ----------------------------
class BuyerModel(models.Model):
    USER_TYPE_CHOICES = (
        ('buyer', 'Buyer'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='buyer')
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


# ----------------------------
# Product Model
# ----------------------------
class Product(models.Model):
    CATEGORY_CHOICES = (
        ('fruit', 'Fruit'),
        ('grain', 'Grain'),
        ('vegetable', 'Vegetable'),
        ('legume', 'Legume'),
        ('spice', 'Spice'),
        ('nut', 'Nuts & Seeds'),
        ('beverage', 'Beverage'),
        ('other', 'Other'),
    )

    farmer = models.ForeignKey(FarmerModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    avater = models.ImageField(upload_to='productIMG/', blank=True , null= True)
    
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.farmer.user.first_name}"
