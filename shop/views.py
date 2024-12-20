from django.shortcuts import render,HttpResponse,redirect
from .models import Product,Contact,Orders,OrderUpadate,Registration
from math import ceil
import json
import razorpay
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from media.PayTm import Checksum
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password 
from paytmchecksum import PaytmChecksum

from django.http import HttpResponse
MERCHANT_KEY = 'kbzk1DSbjiV_03p5'



def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('Phone')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password == cpassword:
           hashed_password = make_password(password)
           registration = Registration(name=name, email=email, Phone=phone, address=address, gender=gender, password=hashed_password, cpassword=hashed_password)
           registration.save()
           return redirect('login')
   
       
        else:
            # If passwords do not match, return an error message
            return HttpResponse("Password and Confirm Password don't match.")
            

    # If GET request, render the registration form
    return render(request, 'shop/Registration.html')
    
        
    


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            # Fetch the user by email
            user = Registration.objects.get(email=email)

            # Check if the password matches
            if check_password(password, user.password):
                # Redirect to home or success page if login is successful
                return redirect('home')  # Replace 'home' with your actual success URL
            else:
                return HttpResponse("Invalid password. Please try again.")
        
        except Registration.DoesNotExist:
            # Handle the case when the user is not found
            return HttpResponse("User does not exist. Please register.")

    # For GET requests, render the login form
    return render(request, 'shop/login.html')

    
def index(request):
    allProds = []
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods }
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n= len(prod)
        nsalides=n//4 + ceil((n/4)-(n//4))
        allProds.append([prod,range(1,nsalides),nsalides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def searchMatch(query,item):
    '''return true only if query matches the item'''
    if query in item.Desc.lower() or query in item.Product_name  or query in item.category.lower():
        return True
    else:       
        return False 

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods }
    for cat in cats:
        prodtemp=Product.objects.filter(category=cat)
        prod= [item for item in prodtemp if searchMatch (query,item )]
        n= len(prod)
        nsalides=n//4 + ceil((n/4)-(n//4))
        if len(prod)!= 0:
           allProds.append([prod,range(1,nsalides),nsalides])
    params = {'allProds':allProds,"msg":""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg':"Please make sure to enter relevant search Query"}
    return render(request, 'shop/search.html', params)

def about(request):
    return render(request,'shop/about.html')
    # return render(request,'shop/about.html')

def contact(request):
    if request.method=="POST":
      
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        Phone=request.POST.get('Phone','')
        message=request.POST.get('message','')
        print(name ,email,Phone,message)
        contact= Contact(name=name,email=email,Phone=Phone,message=message)
        contact.save()
        thank =True
        return render(request,'shop/contact.html',{'thank':thank})
    return render(request,'shop/contact.html')


def tracker(request):
    if request.method == "POST":
        orderid = request.POST.get('orderid', '')
        phone_number = request.POST.get('phone_Number', '')

        try:
            # Fetch order
            order = Orders.objects.filter(order_id=orderid, phone_Number=phone_number)
            if order.exists():
                # Fetch updates
                updates = OrderUpdate.objects.filter(order_id=orderid)
                update_list = []
                for item in updates:
                    update_list.append({'text': item.update_desc, 'time': item.timestamp})

                # Prepare response
                response = {
                    "status": "success",
                    "updates": update_list,
                    "itemsJson": order[0].items_json  # Ensure this is a valid JSON string
                }
                return HttpResponse(json.dumps(response, default=str), content_type="application/json")
            else:
                return HttpResponse('{"status": "noitem"}', content_type="application/json")
        except Exception as e:
            print(f"Error: {e}")  # Debugging output
            return HttpResponse('{"status": "error"}', content_type="application/json")

    return render(request, 'shop/tracker.html')
  



def productView(request ,myid):
    #Fetch the  product using the Id 
    product =Product.objects.filter(id=myid)
    return render(request,'shop/productview.html',{'product':product[0]})



razorpay_client = razorpay.Client(auth=("rzp_test_Jh0DY1bhNltLDf", "KODQrNB95v0aPhn3LIB6sy8C"))
def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        fname = request.POST.get('fname', '')
        lname = request.POST.get('lname', '')
        amount_str = request.POST.get('amount', '')
        # Validate amount
        if not amount_str.isdigit():
            return render(request, 'shop/checkout.html', {'error': 'Invalid amount value'})

        amount = int(amount_str) * 100  # Convert to paise (Razorpay expects amount in paise)
        phone_Number = request.POST.get('phone_Number', '')
        gender = request.POST.get('gender', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        county = request.POST.get('county', '')
        zip_code = request.POST.get('zip_code', '')

        # Save order in the database
        order = Orders(
            items_json=items_json,
            fname=fname,
            lname=lname,
            amount=amount // 100,  # Convert to rupees for storage
            phone_Number=phone_Number,
            gender=gender,
            address=address,
            city=city,
            county=county,
            zip_code=zip_code,
        )
        order.save()

        # Create Razorpay order
        razorpay_order = razorpay_client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1",  # Auto-capture after payment
        })

        # Save Razorpay order ID
        order.razorpay_order_id = razorpay_order['id']
        order.save()

        # Pass the Razorpay order details to the template
        return render(request, 'shop/paytm.html', {
            'order': order,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': "rzp_test_Jh0DY1bhNltLDf",
            'amount': amount,
        })

    return render(request, 'shop/checkout.html')
@csrf_exempt
def handle_razorpay_request(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Get JSON data
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_signature = data.get('razorpay_signature')

            # Verify Razorpay signature
            try:
                razorpay_client.utility.verify_payment_signature({
                    "razorpay_order_id": razorpay_order_id,
                    "razorpay_payment_id": razorpay_payment_id,
                    "razorpay_signature": razorpay_signature,
                })

                # Update order status in the database
                order = Orders.objects.get(razorpay_order_id=razorpay_order_id)
                order.payment_status = "Success"
                order.razorpay_payment_id = razorpay_payment_id
                order.save()

                return JsonResponse({"status": "success"})

            except razorpay.errors.SignatureVerificationError:
                return JsonResponse({"status": "failed", "message": "Signature verification failed"})

        except Exception as e:
            return JsonResponse({"status": "failed", "message": str(e)})

    return JsonResponse({"status": "failed", "message": "Invalid request"})



