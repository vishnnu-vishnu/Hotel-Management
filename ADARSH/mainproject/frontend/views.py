from django.core.checks import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from pip._internal import req
from django.contrib import messages
from frontend.models import signupDb, booktableDb, cartDb, formfillingDb, Checkout,Review
from backend.models import addproductDb, categoryDb
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from mainproject import settings
from django.http import HttpResponse
from django.db import IntegrityError


import hmac
from django.shortcuts import render
import hashlib
from rest_framework import generics,status

from rest_framework.response import Response
from django.db import transaction
import razorpay


def frontpage(request):
    data=addproductDb.objects.all()
    cat=categoryDb.objects.all()
    return render(request,"index.html",{'data':data,'cat':cat})

def menupage(request):
    data = addproductDb.objects.all()
    cat = categoryDb.objects.all()
    return render(request,"menu.html",{'data':data,'cat':cat})

def booktable(request):
    data=signupDb.objects.filter(username=request.session['username'])
    return render(request,"tablebook.html",{'data':data})


def aboutpage(request):
    return render(request,"about.html")

def loginpage(request):
    return render(request,"login.html")

def signupsave(request):
    if request.method=="POST":
        un=request.POST.get('username')
        pw=request.POST.get('password')
        em=request.POST.get('email')
        pn=request.POST.get("Pincode")
        obj=signupDb(username=un,password=pw,email=em,Pincode=pn)
        obj.save()
    return redirect(loginpage)


def loginuserpage(request):
    if request.method == "POST":
        un = request.POST.get('Username')
        pw = request.POST.get('Password')
        if signupDb.objects.filter(username=un, password=pw).exists():
            request.session['username'] = un
            request.session['password'] = pw
            messages.success(request, "Login successful")
            return redirect(frontpage)  # Assuming frontpage is the name of the URL pattern for your front page
        else:
            messages.error(request, "Incorrect username or password! Please try again...")
            return redirect(loginpage)  # Assuming loginuserpage is the name of the URL pattern for your login page
    else:
        return render(request, 'login.html')

def savetable(request):
    if request.method=="POST":
        tn=request.POST.get('oname')
        nn=request.POST.get('ophone')
        te=request.POST.get('oemail')
        tp=request.POST.get('number')
        td=request.POST.get('date')
        ft=request.POST.get('fromtime')
        tt=request.POST.get('totime')
        try:
            obj = booktableDb(name=tn, number=nn, email=te, persons=tp, date=td, fromtime=ft, totime=tt)
            obj.save()
        except IntegrityError:
            messages.error(request, "Table Not Available for the selected time range. Please choose a different time.")
            return redirect(booktable)  
        subject = 'Table Booked'
        message = 'your Table Booked successfully  Table'  f'{tp}'
        from_email = 'subinalangottu@gmail.com'
        recipient_list = [te]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        messages.success(request, "Table booked successfully")
        return redirect(frontpage)


def cartpage(request):
    data=cartDb.objects.filter(name=request.session['username'])
    cat=signupDb.objects.filter(username=request.session['username'])
    return render(request,"cart.html",{'data':data,'cat':cat})

def filterpage(request,cate):
    data = addproductDb.objects.filter(productcategory=cate)
    cat = categoryDb.objects.all()
    return render(request,"filter.html",{'data':data,'cat':cat})


def savetocart(request):
    if request.method == "POST":
        na = request.POST.get('name')
        ci = request.POST.get('citem')
        cp = request.POST.get('cprice')
        cq = request.POST.get('cquantity')
        tot = request.POST.get('ctotal')

        # Check if 'ctotal' is not empty before converting to float
        if tot:
            try:
                tot = float(tot)
            except ValueError:
                # Handle the case where 'ctotal' cannot be converted to float
                # You may want to log this error or handle it in a different way
                pass
        else:
            # Handle the case where 'ctotal' is empty
            # You may want to set a default value or handle it in a different way
            pass

        # Check if the item already exists in the cart
        existing_item = cartDb.objects.filter(item=ci, name=na).first()
        if existing_item:
            # If the item exists, update the quantity
            existing_item.quantity += int(cq)
            existing_item.total += tot  # Use the converted total value
            existing_item.save()
        else:
            # If the item doesn't exist, create a new entry
            obj = cartDb(item=ci, price=cp, quantity=cq, name=na, total=tot)
            obj.save()

        messages.success(request, "Added to Cart")
        return redirect('cartpage')  # Assuming 'cartpage' is the name of your cart page URL


def singleproduct(request,dataid):
    data=addproductDb.objects.get(id=dataid)
    return render(request,"singleproduct.html",{'data':data})

def deletecart(request,dataid):
    x=cartDb.objects.get(id=dataid)
    x.delete()
    return redirect(cartpage)

def formfilling(request,razorpay_order_id=None):
    products=cartDb.objects.filter(name=request.session['username'])
    data=signupDb.objects.filter(username=request.session['username'])
    try:
        latest_checkout = Checkout.objects.latest('id')
        razorpay_order_id = latest_checkout.razorpay_order_id
    except Checkout.DoesNotExist:
        razorpay_order_id = None
    return render(request, "formfilling.html",{'data':data,'products':products,'razorpay_order_id': razorpay_order_id})

def saveform(request):
    if request.method == "POST":
        fn = request.POST.get('name')
        fa = request.POST.get('address')
        fe = request.POST.get('email')
        fp = request.POST.get('phone')
        obj = formfillingDb(name=fn,address=fa,email=fe,phone=fp)
        obj.save()
        subject = 'Order Placed'
        message = 'your Order Placed successfully'
        from_email = 'subinalangottu@gmail.com'
        recipient_list = [fe]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        messages.success(request, "Order placed.Thankyou")
    return redirect(frontpage)

def logoutfun(request):
    del request.session[ 'username']
    del request.session['password']
    return redirect(loginuserpage)

def profilepage(request):
    data=signupDb.objects.filter(username=request.session['username'])
    return render(request,"profilepage.html",{'data':data})

def editprofile(request,dataid):
    user=signupDb.objects.get(id=dataid)
    return render(request,"editprofile.html",{'user':user})

def updateprofile(request,dataid):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        gender=request.POST.get('gender')
        House_No=request.POST.get('House_No')
        street=request.POST.get('street')
        City=request.POST.get('City')
        Pincode=request.POST.get('Pincode')
        if Pincode != '679103':
            messages.error(request, "Sorry, delivery is not available to this address.")
            return redirect('profilepage')
        signupDb.objects.filter(id=dataid).update(username=name,email=email,mobile=mobile,gender=gender,House_No=House_No,street=street,City=City,Pincode=Pincode)
        return redirect(profilepage)


import razorpay
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from .models import Checkout, cartDb

def savecheckout(request):
    if request.method == "POST":
        item = request.POST.get('item')
        qty = request.POST.get('qty')
        total = request.POST.get('total')
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        # Create a Checkout object without saving it yet
        checkout_obj = Checkout(item=item, qty=qty, total=total,name=name,email=email,phone=mobile,address=address)

        # Initialize Razorpay client with your API keys
        razorpay_client = razorpay.Client(auth=("rzp_test_amadi2V7sZT2aT", "r2HO6MOLYj1wNjUdKJoJfHBe"))

        # Prepare order data for Razorpay
        order_amount = float(total) * 100  # Convert to paise (Razorpay expects amount in smallest currency unit)
        order_data = {
            'amount': order_amount,
            'currency': 'INR',  # Use the appropriate currency code
            'receipt': 'order_receipt_{}'.format(item),
            'payment_capture': 1  # Auto-capture payment
        }

        try:
            # Create the order on Razorpay
            order_response = razorpay_client.order.create(order_data)
            razorpay_order_id = order_response['id']
            checkout_obj.razorpay_order_id = razorpay_order_id
            checkout_obj.save()  # Save the Checkout object with Razorpay order ID
        except Exception as e:
            print(e)
            return HttpResponseBadRequest('Error creating Razorpay order')

        # Clear items from the cart after successful checkout
        cart_items = cartDb.objects.filter(name=request.session.get('username'))
        cart_items.delete()

        # Redirect user to the formfilling page after successful checkout
        return redirect('formfilling')

    else:
        return HttpResponseBadRequest('Invalid request method')



razorpay_client = razorpay.Client(auth=("rzp_test_dGbzyUivWJNxDV", "4iYJQWiT6WT7xYcl1JdHSD3a"))

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        item_name = request.POST.get('item')
        qty = request.POST.get('qty')
        total = request.POST.get('total')

        try:
            # Search for the product using its name
            product = addproductDb.objects.get(productname=item_name)
        except addproductDb.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=400)

        order_amount = int(total * 100)  # Convert to paise (Razorpay expects amount in smallest currency unit)

        order_data = {
            'amount': order_amount,
            'currency': 'INR',  # Use the appropriate currency code
            'receipt': 'order_receipt_{}'.format(item_name),
            'payment_capture': 1  # Auto-capture payment
        }

        razorpay_client = razorpay.Client(auth=("rzp_test_dGbzyUivWJNxDV", "4iYJQWiT6WT7xYcl1JdHSD3a"))

        try:
            order_response = razorpay_client.order.create(order_data)
            razorpay_order_id = order_response['id']
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Error creating Razorpay order'}, status=500)

        # Create the order object
        try:
            with transaction.atomic():
                order = Checkout.objects.create(
                    item=product.name,
                    qty=qty,
                    total=total,
                    razorpay_order_id=razorpay_order_id
                )
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Error creating order'}, status=500)

        return JsonResponse({'razorpay_order_id': razorpay_order_id})

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


class PaymentCallbackView(generics.GenericAPIView):


   



    def post(self, request, *args, **kwargs):
        # Extract relevant information from the Razorpay callback
        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_signature = request.data.get('razorpay_signature')

        # Verify the payment signature
        secret = settings.RAZORPAY_WEBHOOK_SECRET.encode('utf-8')
        payload = razorpay_order_id.encode('utf-8') + b"|" + razorpay_payment_id.encode('utf-8')
        expected_signature = hmac.new(secret, payload, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(expected_signature, razorpay_signature):
            return Response({'error': 'Invalid Razorpay signature'}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize Razorpay client with your API keys
        razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Fetch the corresponding order from the database
        try:
            order = Checkout.objects.get(razorpay_order_id=razorpay_order_id)
        except Checkout.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check the payment status
        try:
            payment = razorpay_client.payment.fetch(razorpay_payment_id)
            payment_status = payment['status']
        except Exception as e:
            print(e)
            return Response({'error': 'Error fetching payment status'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if payment_status == 'captured':
            # Update your order status or perform other actions as needed
            order.is_paid = True
            order.save()
            return Response({'status': 'Payment successful'})
        else:
            # Handle payment failure or other cases
            return Response({'status': 'Payment failed'}, status=status.HTTP_400_BAD_REQUEST)
        



def delete_latest_checkout(request):
    try:
        latest_checkout = Checkout.objects.latest('id')
        latest_checkout.delete()
        return redirect(frontpage)
    except Checkout.DoesNotExist:
        return redirect(frontpage)
    

def tracking(request):
    data=Checkout.objects.filter(name=request.session['username'])
    return render (request,"tracking.html",{'data':data})



def signuppage(request):
    return render(request,"signup.html")



def submit_review(request):
    if request.method=="POST":
        user_id=request.POST.get('userid')
        user_name=request.POST.get('username')
        review=request.POST.get('rating')
        comment=request.POST.get('comment')
        obj=Review(userid=user_id,username=user_name,rating=review,comment=comment)
        obj.save()
        return redirect(frontpage)
    
    










