# Generated by Django 5.0.1 on 2024-03-10 06:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0020_rename_address_signupdb_city_signupdb_house_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signupdb',
            name='mobile',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1000000000), django.core.validators.MaxValueValidator(9999999999)]),
        ),
    ]
