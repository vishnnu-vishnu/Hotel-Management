# Generated by Django 5.0.1 on 2024-03-02 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0018_alter_checkout_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='status',
            field=models.CharField(default='Processing', max_length=500),
        ),
    ]