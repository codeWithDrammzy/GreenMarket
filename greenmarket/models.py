from django.db import models

class FarmerModel(models.Model):
    USER_TYPE_CHOICES = (
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)
    pass1 = models.CharField(max_length=128)
    pass2 = models.CharField(max_length=128)  # Not recommended for production

    def __str__(self):
        return f"{self.first_name} ({self.user_type})"

from django.db import models

class FarmProduct(models.Model):  # <-- You need this
    Category_Choice = (
        ('fruit', 'Fruit'),
        ('grains', 'Grains'),
        ('vegetables', 'Vegetables'),
        ('legumes', 'Legumes'),
        ('nuts', 'Nuts & Seeds'),
        ('spices', 'Spices & Herbs'),
        ('beverages', 'Beverages'),
        ('others', 'Others'),
    )

    product_name = models.CharField(max_length=50)
    product_price = models.CharField(max_length=50)
    product_category = models.CharField(choices=Category_Choice, max_length=50)
    product_description = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product_name} ({self.product_price})"
