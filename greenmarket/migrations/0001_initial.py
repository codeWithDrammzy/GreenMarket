# Generated by Django 5.2.4 on 2025-07-25 21:57

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BuyerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('buyer', 'Buyer')], default='buyer', max_length=10)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('gender', models.CharField(blank=True, choices=[('F', 'female'), ('M', 'male')], null=True)),
                ('adress', models.CharField(blank=True, max_length=500, null=True)),
                ('state', models.CharField(choices=[('Abia', 'Abia'), ('Adamawa', 'Adamawa'), ('Akwa Ibom', 'Akwa Ibom'), ('Anambra', 'Anambra'), ('Bauchi', 'Bauchi'), ('Bayelsa', 'Bayelsa'), ('Benue', 'Benue'), ('Borno', 'Borno'), ('Cross River', 'Cross River'), ('Delta', 'Delta'), ('Ebonyi', 'Ebonyi'), ('Edo', 'Edo'), ('Ekiti', 'Ekiti'), ('Enugu', 'Enugu'), ('Gombe', 'Gombe'), ('Imo', 'Imo'), ('Jigawa', 'Jigawa'), ('Kaduna', 'Kaduna'), ('Kano', 'Kano'), ('Katsina', 'Katsina'), ('Kebbi', 'Kebbi'), ('Kogi', 'Kogi'), ('Kwara', 'Kwara'), ('Lagos', 'Lagos'), ('Nasarawa', 'Nasarawa'), ('Niger', 'Niger'), ('Ogun', 'Ogun'), ('Ondo', 'Ondo'), ('Osun', 'Osun'), ('Oyo', 'Oyo'), ('Plateau', 'Plateau'), ('Rivers', 'Rivers'), ('Sokoto', 'Sokoto'), ('Taraba', 'Taraba'), ('Yobe', 'Yobe'), ('Zamfara', 'Zamfara'), ('FCT', 'Federal Capital Territory')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FarmerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('farmer', 'Farmer')], default='farmer', max_length=10)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_paid', models.BooleanField(default=False)),
                ('is_delivered', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('paid', 'Paid')], default='pending', max_length=20)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('order_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='greenmarket.buyermodel')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('fruit', 'Fruit'), ('grain', 'Grain'), ('vegetable', 'Vegetable'), ('legume', 'Legume'), ('spice', 'Spice'), ('nut', 'Nuts & Seeds'), ('beverage', 'Beverage'), ('other', 'Other')], max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True)),
                ('avater', models.ImageField(blank=True, null=True, upload_to='productIMG/')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='greenmarket.farmermodel')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='greenmarket.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='greenmarket.product')),
            ],
        ),
    ]
