# Generated by Django 4.2.1 on 2023-05-12 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='featured_image',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
