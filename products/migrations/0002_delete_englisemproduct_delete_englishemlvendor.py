# Generated by Django 4.2.1 on 2023-05-24 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EnglisemProduct',
        ),
        migrations.DeleteModel(
            name='EnglishemlVendor',
        ),
    ]
