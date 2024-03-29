# Generated by Django 4.2.1 on 2023-06-13 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('slug', models.SlugField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=200)),
                ('variant_id', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('sku', models.CharField(max_length=200, unique=True)),
                ('handle', models.CharField(max_length=200)),
                ('price_englishelm', models.CharField(blank=True, max_length=200)),
                ('price_livaroom', models.CharField(blank=True, max_length=200)),
                ('barcode', models.CharField(max_length=200)),
                ('featured_image', models.CharField(blank=True, max_length=200)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='products.category')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='products.vendor')),
            ],
        ),
    ]
