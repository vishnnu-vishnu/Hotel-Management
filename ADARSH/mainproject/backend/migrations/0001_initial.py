# Generated by Django 4.2.6 on 2023-11-08 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='categoryDb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryname', models.CharField(blank=True, max_length=100, null=True)),
                ('categorydescription', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
