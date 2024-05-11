from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.core.exceptions import ValidationError

# Create your models here.
class signupDb(models.Model):
    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    House_No = models.CharField(max_length=250, null=True, blank=True)
    street = models.CharField(max_length=250, null=True, blank=True)
    City = models.CharField(max_length=250, null=True, blank=True)
    Pincode = models.CharField(max_length=250, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.IntegerField(
        validators=[
            MinValueValidator(1000000000),  # 10-digit minimum
            MaxValueValidator(9999999999),  # 10-digit maximum
        ],
        null=True,
        blank=True
    )

    def clean(self):
        # Restrict registration to only '679103' Pincode
        allowed_pincode = '679103'
        if self.Pincode != allowed_pincode:
            raise ValidationError('Only users from Pincode 679103 are allowed to register.')

    def save(self, *args, **kwargs):
        self.clean()  # Ensure the model is clean before saving
        super().save(*args, **kwargs)

class booktableDb(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    number = models.IntegerField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    persons = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(max_length=100, blank=True, null=True)
    fromtime=models.TimeField(null=True)
    totime=models.TimeField(null=True)


    def clean(self):
        # Check if there are any bookings inside the time range
        conflicting_bookings = booktableDb.objects.filter(
            date=self.date,
            fromtime=self.totime,
            totime=self.fromtime,
            persons=self.persons
        ).exclude(pk=self.pk)  # Exclude current instance if it's being updated

        if conflicting_bookings.exists():
            raise ValidationError('There is a conflicting booking for the selected time range.')

    class Meta:
        # Ensure uniqueness in the same date and time range
        unique_together = ('date', 'fromtime', 'totime','persons')


class cartDb(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    item = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(max_length=100, blank=True, null=True)
    total = models.IntegerField(max_length=100, blank=True, null=True)

class formfillingDb(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.IntegerField(max_length=100, blank=True, null=True)

class Checkout(models.Model):
    name=models.CharField(max_length=500,null=True,blank=True)
    email=models.EmailField(max_length=500,null=True,blank=True)
    phone=models.CharField(max_length=500,null=True,blank=True)
    address=models.CharField(max_length=500,null=True,blank=True)
    item=models.CharField(max_length=500,null=True,blank=True)
    qty=models.IntegerField(max_length=100,null=True,blank=True)
    total=models.DecimalField(max_digits=10,max_length=100,null=True,blank=True,decimal_places=2)
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    status=models.CharField(max_length=500,default="Processing")



class Review(models.Model):
    userid=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    rating=models.CharField(max_length=100)
    comment=models.CharField(max_length=300)

