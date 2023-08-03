from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader
from .models import *
import json
from .form import CustomUserForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def home(request):
    products=Product.objects.filter(Trending=1)
    template=loader.get_template('myApp/index.html')
    return HttpResponse(template.render({'products':products},request))

def cart_page(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        template=loader.get_template('myApp/cart.html')
        return HttpResponse(template.render({'cart':cart},request))
    else:
        return redirect("/")
    
def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")

def remove_fav(request,cid):
    cartitem=Favourite.objects.get(id=cid)
    cartitem.delete()
    return redirect("/favviewpage")

def favviewpage(request):
    if request.user.is_authenticated:
        fav=Favourite.objects.filter(user=request.user)
        template=loader.get_template('myApp/fav.html')
        return HttpResponse(template.render({'fav':fav},request))
    else:
        return redirect("/")


def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=(data['product_qty'])
            product_id=(data['pid'])
            
            print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                     return JsonResponse({'status':'Product Already in Cart Success'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product Added to Cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product stock not available'},status=200)
          
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)
    

def fav_page(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
           
            product_id=(data['pid'])
            product_status=Product.objects.get(id=product_id)
            
            print(request.user.id)
            if product_status:
                if Favourite.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status':'Product Already in Favourite'},status=200)
                else:
                    Favourite.objects.create(user=request.user,product_id=product_id)
                    return JsonResponse({'status':'Product Added to favourite'},status=200)
        else:
            return JsonResponse({'status':'Login to Add favourite'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged out sucessfully")
    return redirect('/')

def login_page(request):
    if request.user.is_authenticated:
         return redirect('/')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('Password')
            user = authenticate(request, username=name, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully")
                return redirect('/')
            else:
                messages.error(request, "Invalid User Name or Password")
        template=loader.get_template('myApp/login.html')
        return HttpResponse(template.render({},request))

def register(request):
    form= CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Sucess you can login Now..!")
            return redirect('/login/')
    template=loader.get_template('myApp/register.html')
    return HttpResponse(template.render({'form':form},request))

def collections(request):
    categories = Catagory.objects.filter(status=0)  # Update the model name here as well
    template = loader.get_template('myApp/collections.html')
    return HttpResponse(template.render({"category": categories}, request))  # Use "category" instead of "catagory"

def collectionview(request, name):
    if Catagory.objects.filter(name=name, status=0).exists():
        product = Product.objects.filter(catagory__name=name)
        template = loader.get_template('myApp/collectionview.html')
        return HttpResponse(template.render({"products": product , "catagory":name}, request))
    else:
        messages.warning(request, "No such Category found")
        return redirect('collections')

def Product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
          product = Product.objects.filter(name=pname,status=0).first()
          template = loader.get_template('myApp/product_details.html')
          return HttpResponse(template.render({"product": product}, request))
        else:
            messages.error(request,"Sorry! No Such Product Found.")
            return redirect('collections')
    else:
        messages.error(request, "No such Category found")
        return redirect('collections')

