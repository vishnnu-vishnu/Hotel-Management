# Generated by Django 4.2.6 on 2023-11-20 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_addproductdb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addproductdb',
            name='productimg',
            field=models.ImageField(blank=True, null=True, upload_to='PRODUCT'),
        ),
    ]
