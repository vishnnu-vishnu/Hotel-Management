from django.db import models

# Create your models here.


class categoryDb(models.Model):
    categoryname = models.CharField(max_length=100,blank=True,null=True)
    categorydescription = models.CharField(max_length=100,blank=True,null=True)


class addproductDb(models.Model):
    productname = models.CharField(max_length=100,blank=True,null=True)
    productcategory = models.CharField(max_length=100,blank=True,null=True)
    productdescription = models.CharField(max_length=100,blank=True,null=True)
    productimg = models.ImageField(upload_to="PRODUCT",blank=True,null=True)
    productprice = models.IntegerField(max_length=100,blank=True,null=True)

class table(models.Model):
    tablename=models.CharField(max_length=150,blank=True,null=True)
    capacity=models.IntegerField(max_length=10,null=True,blank=True)

