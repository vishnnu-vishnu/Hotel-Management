# Generated by Django 5.0.1 on 2024-03-02 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0017_checkout_address_checkout_email_checkout_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='status',
            field=models.CharField(default='Processing', max_length=200),
        ),
    ]
