# Generated by Django 5.2.4 on 2025-07-13 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('greenmarket', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FarmProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('product_price', models.CharField(max_length=50)),
                ('product_category', models.CharField(max_length=50)),
                ('product_description', models.CharField(max_length=50)),
            ],
        ),
    ]
