from django.shortcuts import render,redirect,HttpResponse
# mesages library
from django.contrib import messages
# authentication libary
from django.contrib.auth import authenticate,login,logout
# getting user model
from django.contrib.auth.models import User
# decorators
from django.contrib.auth.decorators import login_required

from django.conf import settings
  
# getting items from database
from base.models import Product,Contact,Orders,OrderUpdate
# math library
from math import ceil
# merchant key importation
from base import keys
import json
from django.views.decorators.crsf import crsf_exempt

from PayTm import Checksum
# merchant key /MERCHANT_KEY ="" is another method of passing merchant key
MERCHANT_KEY = keys.MK
# install pycryptodome

# Create your views here.
# home function cateogrizing items
def home(request):
    return render(request,'index.html')

# purchase function cateogrizing items
def purchase(request):
    # getting authenticated curent user and printing it
    #current_user = request.user
    #print(current_user) 
    # products list
    allproducts = []
    # categorizing products using category & id
    categorizeproducts = Product.objects.values('category','id')
    #passing products as alist in dictionary
    categories = {item['category'] for item in categorizeproducts}
    # filtering all cartegories
    for categgory in categories:
        productt= Product.objects.filter(category=categgory)
        # displaying four products in a row using a formula
        n=len(productt)
        # four item formula
        nSlides = n//4 + ceil((n/4)-(n//4))
        allproducts.append([productt,range(1,nSlides),nSlides])
    parametter = {'allproducts':allproducts }
    return render(request,'purchase.html',parametter)

#checkout function
def checkout(request):
    # checking if user is authenticated
    if not request.user.is_authenticated:
        messages.warning(request,"Login and try again")
        return redirect('/baseauth/login')
    if request.method == "POST":
        # Getting clients detail
        # items clients has order
        item_json = request.POST.get('itemsJson','')
        name = request.POST.get('name','')
        amount = request.POST.get('amt')
        email = request.POST.get('email','')
        address1 = request.POST.get('address1','')
        address2 = request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zipcode = request.POST.get('zipcode','')
        phone = request.POST.get('phone','')
        
        # ORDERING ITEMS
        # creating one Orders database table for storing all items in an order
        Order = Orders(items_json=items_json,name=name,amount=amount,email=email,address1=address1,address2=address2,city=city,state=state,zipcode=zipcode,phone=phone)
        
        print(amount)
        Order.save()
        # order update table and passing the order id and updating a string ,and saving automatically while informing the order has been updated
        update = OrderUpdate(order_id=Order.order_id,update_desc="The order has been placed")
        update.save()
        thank = True
        # start of PAYMENT INTERGARTION
        # getting the generated order id
        id = Order.order_id
        #converting order id into string,as online transaction is automatically tokens generated is in form of strings a mixture of numbers and letters thus needs to be converted to strings
        # appending string to make an order id unique & easily identify
        oid = str(id) + "OREM "
        # mid=merchad id
        # during production 'WEBSITE':'WEB-WEB'
        param_dict = {
            'MID':keys.MID,
            'ORDER_ID':oid,
            'TXN_AMOUNT':str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSITESTAGING',
            'CHANNEL_ID':'WEB',
            'CALLBACK_URL':'http//127.0.0.1:8000/handlerequest/',
        }
        # Passing checksum data which will go to handlerequest
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request,'paytm.html',{'param_dict':param_dict})
        
    return render(request,'checkout.html')

# tracking function 
def tracker(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/login')
    #
    if request.method == 'POST':
        orderId = request.POST.get('orderId','')
        email = request.POST.get('email','')
        #
        try:
            order = Order.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                update = []
                #
                for item in update:
                    updates.append({'text':item.update desc, 'time': item.timestamp}, response = json.dumps([updates,orders[0].items_json], default=str))
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
    return render(request,'tracker.html')

# product view function
def productView(request,myid):
    # fetch product using  the id
    product = product.objects.filter(id=myid)
    
    return render(request,   'prodView.html',{'product':product[0]})
    
# login function
@crsf_exempt
def handlerequest(request):
    # paytm will take it as a post form and send it paytm to generate checksum then  paytm will send you post request here
    form = request.POST
    response_dict = {}
    # taking all the keys value
    for i in form.keys():
        response_dict[i] = form[i]
        # checking if responses are equal to checksumhash
        if i == 'CHECKSUMHASH':
            # storing all the values in checksum file
            checksum = form[i]
    # verifying the checksum file
    verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        # successful order
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            a=response_dict['ORDERID']
            b=response_dict['TXNAMOUNT']
            # replacing the appende word with nothing
            rid=a.replace("orem","")
            
            print(rid)
            # extracting order id with response id
            filter2 = Orders.objects.filter(order_id=rid)
            print(filter2)
            print(a,b)
            
            # saving 
            for post1 in filter2:
                #apding the info in database
                post1.oid = a
                post1.amountpaid = b
                post1.paymentstatus = "PAID"
                post1.save()
            print("Run agede function")
        else:
            # response mesage incase its not successful and the eror
            print("Order was not successful because" + response_dict['RESPMSG'])
    return render(request,'paymentstatus.html',{'response':response_dict})
                
                
                
# logout function
def logouts(request):
    logout(request)
    messages.warning(request,"Logout Successfuly")
    return render(request,'login.html')

# login function
def handlelogin(request):
    if request.method == 'POST':
        # getting user parameter
        loginusername = request.POST['email']
        loginpassword = request.POST['password1']
        user = authenticate(username=loginusername,password=loginpassword)
        
        #
        if user is not None:
            login(request,user)
            messages.info(request,"logged in Successfully")
            return redirect('/')
        else:
            messages.error(request,"Invalid credentials")
            return redirect('/login  ')
        