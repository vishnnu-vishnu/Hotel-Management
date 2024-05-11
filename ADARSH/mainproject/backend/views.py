from django.shortcuts import render,redirect
from frontend.models import Checkout,Review,booktableDb
from backend.models import categoryDb,addproductDb,table
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.

def home(request):
    data=Checkout.objects.all()
    return render(request,"home.html",{'data':data})

def category(request):
    cat=categoryDb.objects.all()
    return render(request,"addcategory.html",{'cat':cat})

def savecategory(request):
    if request.method=="POST":
        cn=request.POST.get('categoryName')
        cd=request.POST.get('categoryDescription')
        obj=categoryDb(categoryname=cn,categorydescription=cd)
        obj.save()
    return redirect(category)

def display(request):
    data=categoryDb.objects.all()
    return render(request, "display category.html",{'data':data})




def saveproducts(request):
    if request.method=="POST":
        pn=request.POST.get('ProductName')
        pd=request.POST.get('description')
        pc=request.POST.get('ProductCategory')
        pi=request.FILES['ProductImg']
        pp=request.POST.get('ProductPrice')
        obj=addproductDb(productname=pn,productcategory=pc,productimg=pi,productprice=pp,productdescription=pd)
        obj.save()
    return redirect(category)


def product(request):
    data=addproductDb.objects.all()
    return render(request, "display product.html",{'data':data})


def deletepro(request,dataid):
    obj=addproductDb.objects.get(id=dataid)
    obj.delete()
    return redirect(product)

def editpro(request,dataid):
    data=addproductDb.objects.get(id=dataid)
    cat = categoryDb.objects.all()
    return render(request, "editpage.html",{'data':data,'cat':cat})

def updatepro(request,dataid):
    if request.method=="POST":
        pn=request.POST.get('ProductName')
        pc=request.POST.get('ProductCategory')
        pp=request.POST.get('ProductPrice')
        pd=request.POST.get('description')
        try:
            img=request.FILES['img']
            fs=FileSystemStorage()
            file=fs.save(img.name,img)
        except MultiValueDictKeyError:
            file=addproductDb.objects.get(id=dataid).productimg
        addproductDb.objects.filter(id=dataid).update(productname=pn,productdescription=pd,productcategory=pc,productprice=pp,productimg=file)
        return redirect(product)

def addtable(request):
    if request.method=="POST":
        tn=request.POST.get('TableName')
        tc=request.POST.get('Tablecapacity')
        obj=table(tablename=tn,capacity=tc)
        obj.save()
        return redirect(category)
    
def updatestatus(request,dataid):
    if request.method=="POST":
        s=request.POST.get('approve')
        Checkout.objects.filter(id=dataid).update(status=s)
        return redirect(home)


from datetime import date


def display_tablebooking(request):
    today = date.today()
    data=booktableDb.objects.filter(date=today)
    return render(request,"tablebooking.html",{'data':data})

def display_rating(request):
    data=Review.objects.all()
    return render(request,"displayrating.html",{'data':data})





