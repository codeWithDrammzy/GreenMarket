from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    Gender = (
        ('F', 'female'),
        ('M', 'male')
    )
    STATE_CHOICES = [
    ('Abia', 'Abia'),
    ('Adamawa', 'Adamawa'),
    ('Akwa Ibom', 'Akwa Ibom'),
    ('Anambra', 'Anambra'),
    ('Bauchi', 'Bauchi'),
    ('Bayelsa', 'Bayelsa'),
    ('Benue', 'Benue'),
    ('Borno', 'Borno'),
    ('Cross River', 'Cross River'),
    ('Delta', 'Delta'),
    ('Ebonyi', 'Ebonyi'),
    ('Edo', 'Edo'),
    ('Ekiti', 'Ekiti'),
    ('Enugu', 'Enugu'),
    ('Gombe', 'Gombe'),
    ('Imo', 'Imo'),
    ('Jigawa', 'Jigawa'),
    ('Kaduna', 'Kaduna'),
    ('Kano', 'Kano'),
    ('Katsina', 'Katsina'),
    ('Kebbi', 'Kebbi'),
    ('Kogi', 'Kogi'),
    ('Kwara', 'Kwara'),
    ('Lagos', 'Lagos'),
    ('Nasarawa', 'Nasarawa'),
    ('Niger', 'Niger'),
    ('Ogun', 'Ogun'),
    ('Ondo', 'Ondo'),
    ('Osun', 'Osun'),
    ('Oyo', 'Oyo'),
    ('Plateau', 'Plateau'),
    ('Rivers', 'Rivers'),
    ('Sokoto', 'Sokoto'),
    ('Taraba', 'Taraba'),
    ('Yobe', 'Yobe'),
    ('Zamfara', 'Zamfara'),
    ('FCT', 'Federal Capital Territory'),
]


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='buyer')
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(choices=Gender ,blank= True, null=True)
    adress = models.CharField(max_length=500, blank=True, null=True)
    state = models.CharField(choices= STATE_CHOICES)

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


# ----------------------------
# Order Model
# ----------------------------
class Order(models.Model):
    buyer = models.ForeignKey(BuyerModel, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order #{self.id} by {self.buyer.user.get_full_name()}"
    

# ----------------------------
# Item_Order Model
# ----------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.price
