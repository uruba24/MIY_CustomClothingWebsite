import array
from importlib import import_module
from turtle import title
import_module 
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from django.views import  View, generic
import razorpay
from app.admin import NeckSleevesModelAdmin
from .models import CATEGORY_CHOICES, Basket, Bottoms, Budget, Customer, Necks, Product , Cart,  OrderPlaced , Fabric, Colors, Shapes, Colorshape, Necks, Shapeneck, Sleeve, Necksleeves, Bottoms, Order , OrderItem, Budget, Recommendation
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse, request, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core import serializers
import random
from django.views.decorators.csrf import csrf_exempt
from MIY.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
json_serializer = serializers.get_serializer("json")()



#def home(request):
 #return render(request, 'app/home.html')

class ProductView(View):
     def get(self, request):
        totalitem = 0
        bags = Product.objects.filter(category='B')
        Shoes = Product.objects.filter(category='S')
        Bottom = Product.objects.filter(category='Bm')
        Seperates= Product.objects.filter(category='Se')
        if request.user.is_authenticated:
          totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/home.html',{'bags':bags, 'Shoes' :Shoes, 'Bottom':Bottom, 'Seperates':Seperates, 'totalitem':totalitem})

#def product_detail(request):
 #return render(request, 'app/productdetail.html')


class ProductDetailView(View):
 def get(self, request, pk):
    totalitem = 0
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    return render(request, 'app/productdetail.html',
     {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})

@login_required
def add_to_cart(request):
 prod = Product()
 user=request.user
 id = request.GET.get('id', "")
 price = request.GET.get('price', "")
 type = request.GET.get("type", "")
 sleeves_img = request.GET.get("image", "") 
 reduced_string = sleeves_img[6:]
 fabric_id = request.GET.get('fabric_id', "")
 color_id = request.GET.get('color_id', "")
 shape_id = request.GET.get('shape_id', "")
 neck_id = request.GET.get('neck_id', "")
 sleeve_id = request.GET.get('sleeve_id', "")
 print(reduced_string)
 if type == "custom":
   #  addproduct = Product(title="customize product", selling_price=price, discounted_price="6000", description= "dtikjl,,kjjkgtrdffcfv", brand="Velvet", category="Seperates", product_image=reduced_string).save()
    new_product = Product()
    new_product.title = "customize product"
    new_product.selling_price = int(price)
    new_product.discounted_price = str(int(price) / 100 * 20)
    new_product.description = "lorem ipsum"
    new_product.brand = "Velvet"
    new_product.category = "customized"
    new_product.product_image = reduced_string
    new_product.attribute_ids = "{}_{}_{}_{}_{}".format(fabric_id, color_id, shape_id, neck_id, sleeve_id)
    new_product.save()
    product_id = new_product.id
    product = Product.objects.get(id=product_id)
   
 else:
    product_id = request.GET.get('prod_id') 
    product = Product.objects.get(id=product_id)
 
 Cart(user=user, product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
   totalitem = 0
   if request.user.is_authenticated:
      user = request.user
      cart = Cart.objects.filter(user=user)
      print(cart)
      amount = 0.0
      shipping_amount = 0.0
      total_amount = 0.0
      cart_product = [p for p in Cart.objects.all() if p.user == user]
      if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
      print(cart_product)
      if cart_product:
         recommendProducts = []

         customized_items = Cart.objects.filter(user=user,product__category='customized')
         for customized_item in customized_items:
           
            if customized_item and customized_item.product and customized_item.product.attribute_ids:
               item = {
                  'product': customized_item.product,
                  'items': []
               }

               [fabric_id, color_id, shape_id, neck_id, sleeve_id] = customized_item.product.attribute_ids.split('_')
               bag = Recommendation.objects.order_by('-bag_counter').filter(~Q(bag=None),fabric=fabric_id,color=color_id).prefetch_related('bag').first() 
               shoe = Recommendation.objects.order_by('-shoe_counter').filter(~Q(shoe=None),fabric=fabric_id,color=color_id).prefetch_related('shoe').first() 
               bottom = Recommendation.objects.order_by('-bottom_counter').filter(~Q(bottom=None),fabric=fabric_id,color=color_id).prefetch_related('bottom').first() 
               separate = Recommendation.objects.order_by('-separate_counter').filter(~Q(separate=None),fabric=fabric_id,color=color_id).prefetch_related('separate').first() 

               if bag: item['items'].append(bag.bag)
               if shoe: item['items'].append(shoe.shoe)
               if bottom: item['items'].append(bottom.bottom)
               if separate: item['items'].append(separate.separate)

               recommendProducts.append(item)

         for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount
            totalamount = amount + shipping_amount
         return render(request, 'app/addtocart.html', {'carts':cart, 'totalamount':totalamount, 'amount':amount, 'totalitem':totalitem, 'recommendProducts':recommendProducts}) 
      else:
         return(request, 'app/emptycart.html')   

def plus_cart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      print(prod_id)
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity+=1
      c.save()
      amount = 0.0
      shipping_amount = 0.0
      total_amount = 0.0
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      print(cart_product)
      if cart_product:
         for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount

      data = {
            'quantity': c.quantity,
           'amount': amount,
           'totalamount' : amount + shipping_amount
         }       
      return JsonResponse(data)

def minus_cart(request):
 
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      print(prod_id)
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity-=1
      c.save()  
      amount = 0.0
      shipping_amount = 0.0
      total_amount = 0.0
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      print(cart_product)
      if cart_product:
         for p in cart_product:
            tempamount = (p.quantity * p.product.selling_price)
            amount += tempamount

         data = {
           'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
         }       
         return JsonResponse(data)    


def remove_cart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.delete()  
      amount = 0.0
      shipping_amount = 0.0
      total_amount = 0.0
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      print(cart_product)
      if cart_product:
       for p in cart_product:
        tempamount = (p.quantity * p.product.selling_price)
        amount += tempamount
         
      data = {
         'amount': amount,
         'totalamount': amount + shipping_amount     
      }       
      return JsonResponse(data)               


def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

@login_required
def address(request):
   totalitem = 0
   add = Customer.objects.filter(user=request.user)
   if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'app/home.html', {'add':add, 'active':'btn-primary', 'totalitem':totalitem})

@login_required
def orders(request):
   totaitem = 0
   orders = Order.objects.filter(user=request.user)
   context = {'orders':orders}
   if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
   return render(request, 'app/myorders.html', context, {'totaitem':totaitem})

def bags(request, data=None):
 totalitem = 0
 if data == None: 
    bags = Product.objects.filter(category='B')
 elif data == 'Handbags' or data == 'Clutches':
    bags = Product.objects.filter(category='B').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/bags.html', {'bags':bags, 'totalitem':totalitem})


def shoes(request, data=None):
 totalitem = 0
 if data == None:
    shoes = Product.objects.filter(category='S')
 elif data == 'Flats' or data == 'Heels':
    shoes = Product.objects.filter(category='S').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/shoes.html', {'shoes':shoes, 'totalitem':totalitem})

@login_required
def bottoms(request, data=None):
 totalitem = 0
 if data == None:
    bottoms = Product.objects.filter(category='Bm')
 elif data == 'Staright-Pants' or data == 'Plazos':
    bottoms = Product.objects.filter(category='Bm').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/bottoms.html', {'bottoms':bottoms, 'totalitem':totalitem})

@login_required
def seperates(request, data=None):
 totalitem = 0
 if data == None:
    seperates = Product.objects.filter(category='Se')
 elif data == 'Strolls' or data == 'Dupatta':
    seperates = Product.objects.filter(category='Se').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/seperates.html', {'seperates':seperates, 'totalitem':totalitem})


class CustomerRegistrationView(View):
  def get(self, request):
   form = CustomerRegistrationForm()
   return render(request, 'app/customerregistration.html', {'form':form})

  def post(self, request):
   form = CustomerRegistrationForm(request.POST)
   if form.is_valid():
    messages.success(request, 'Congratulations!! Registered Successfully')
    form.save()
   return render(request, 'app/customerregistration.html',{'form':form}) 

@login_required
def checkout(request):
  user = request.user
  print(user)
  add = Customer.objects.filter(user=user)
  cart_items = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 70.0
  totalamount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      #print(cart_product) 
  if cart_product:
    for p in cart_product:
      tempamount = (p.quantity * p.product.selling_price)
      dcamount = p.product.discounted_price
      amount += tempamount
    totalamount = amount
  return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items})

#@login_required
#def payment_done(request):
 #  user = request.user
  # custid = request.GET.get('custid')
  # customer = Customer.objects.get(id=custid)
  #cart = Cart.objects.filter(user=user)
   #for c in cart:
    #3  OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
      #c.delete()
  # return redirect("orders")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
   def get(self, request):
      totalitem = 0
      form = CustomerProfileForm()
      if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
      return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})

   def post(self, request):
      form = CustomerProfileForm(request.POST)
      if form.is_valid():
         usr = request.user
         name = form.cleaned_data['name'] 
         locality = form.cleaned_data['locality'] 
         city = form.cleaned_data['city'] 
         state = form.cleaned_data['state']
         zipcode = form.cleaned_data['zipcode'] 
         reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
         reg.save()
         messages.success(request, 'Congratulations!! Profile Updated Successfully')
      return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})  

       
@login_required
def Casual(request, data=None):
  if data == None:
     Casual = Fabric.objects.filter(category='CF')
  return render(request, 'app/CasualFabric.html', {'Casual':Casual})

@login_required
def Festive(request, data=None):
 user=request.user
 price = request.GET.get('price')
 if data == None:
    Festive = Fabric.objects.filter(category='FF')
 if price:
    Festive = Fabric.objects.filter(category='FF').filter(selling_price__lte = price)
 if request.method == 'GET':
    if request.GET.get('price'):
       price=request.GET.get('price')
       Budget(user=user, price=price).save()     
 return render(request, 'app/FestiveFabric.html', {'Festive':Festive, 'price':price})

@login_required
def Luxury(request, data=None):
 price = request.GET.get('price')
 if request.method=='POST':
    if request.POST.get('price'):
       savebudget=Budget()
       savebudget.price=request.POST.get('price')
       savebudget.save()
 if data == None:
    Luxury= Fabric.objects.filter(category='LF')
 if price:
    Luxury = Fabric.objects.filter(category='LF').filter(selling_price__lte = price)
 return render(request, 'app/LuxuryFabric.html', {'Luxury':Luxury})

@login_required
def CFC(request, data=None):
 totalitem = 0
 if data == None:
    CFC = Colors.objects.filter(category='CF')
 elif data == 'Lawn' or data == 'Printed' or data == 'Denim':
    CFC = Colors.objects.filter(category='CF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Lawn.html', {'CFC':CFC, 'totalitem':totalitem})

@login_required
def PFC(request, data=None):
 totalitem = 0
 if data == None:
    PFC = Colors.objects.filter(category='CF')
 elif data == 'Lawn' or data == 'Printed' or data == 'Denim':
    PFC = Colors.objects.filter(category='CF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Printed.html', {'PFC':PFC, 'totalitem':totalitem})

def Denim(request, data=None):
 totalitem = 0
 if data == None:
    Denim = Colors.objects.filter(category='CF')
 elif data == 'Lawn' or data == 'Printed' or data == 'Denim':
    Denim = Colors.objects.filter(category='CF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Denim.html', {'Denim':Denim, 'totalitem':totalitem})

@login_required
def TienDye(request, data=None):
 totalitem = 0
 if data == None:
    TienDye = Colors.objects.filter(category='CF')
 elif data == 'Lawn' or data == 'Printed' or data == 'Denim':
    TienDye = Colors.objects.filter(category='CF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/TieDye.html', {'TienDye':TienDye, 'totalitem':totalitem})

@login_required
def floral(request, data=None):
 totalitem = 0
 if data == None:
    floral = Colors.objects.filter(category='CF')
 elif data == 'Lawn' or data == 'Printed' or data == 'Denim':
    floral = Colors.objects.filter(category='CF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Floral.html', {'floral':floral, 'totalitem':totalitem})

@login_required
def Silk(request, data=None):
 totalitem = 0
 if data == None:
    slk = Colors.objects.filter(category='CF')
 elif data == 'Lawn' or data == 'Printed' or data == 'Denim':
    slk = Colors.objects.filter(category='CF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/silk.html', {'slk':slk, 'totalitem':totalitem})

@login_required
def Cambric(request, data=None):
 totalitem = 0
 if data == None:
    cambric = Colors.objects.filter(category='CF')
 elif data == 'Lawn' or data == 'Printed' or data == 'Denim':
    cambric = Colors.objects.filter(category='CF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Cambric.html', {'cambric':cambric, 'totalitem':totalitem})

@login_required
def Linen(request, data=None):
 totalitem = 0
 if data == None:
    linen = Colors.objects.filter(category='CF')
 elif data == 'Lawn' or data == 'Printed' or data == 'Denim':
    linen = Colors.objects.filter(category='CF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Linen.html', {'linen':linen, 'totalitem':totalitem})

@login_required
def Canva(request, data=None):
 totalitem = 0
 if data == None:
    canva = Colors.objects.filter(category='CF')
 elif data == 'Lawn' or data == 'Printed' or data == 'Denim':
    canva = Colors.objects.filter(category='CF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Canva.html', {'canva':canva, 'totalitem':totalitem})

@login_required
def Nylon(request, data=None):
 totalitem = 0
 if data == None:
    nylon = Colors.objects.filter(category='CF')
 elif data == 'Lawn' or data == 'Printed' or data == 'Denim':
    nylon = Colors.objects.filter(category='CF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Nylon.html', {'nylon':nylon, 'totalitem':totalitem})

@login_required
def RayonC(request, data=None):
 totalitem = 0
 if data == None:
    RayonC = Colors.objects.filter(category='CF')
 elif data == 'Lawn' or data == 'Printed' or data == 'Denim':
    RayonC = Colors.objects.filter(category='CF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/RayonC.html', {'RayonC':RayonC, 'totalitem':totalitem})

@login_required
def Embroidedvelvet(request, data=None):
 totalitem = 0
 if data == None:
    Embroidedvelvet = Colors.objects.filter(category='LF')
 elif data == 'EmbroidedVelvet' or data == 'Sequence' or data == 'tule':
   Embroidedvelvet = Colors.objects.filter(category='LF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/embvelvet.html', {'Embroidedvelvet':Embroidedvelvet, 'totalitem':totalitem})

@login_required
def Seq(request, data=None):
 totalitem = 0
 if data == None:
    Seq = Colors.objects.filter(category='LF')
 elif data == 'EmbroidedVelvet' or data == 'Sequence' or data == 'tule':
   Seq = Colors.objects.filter(category='LF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/sequence.html', {'Seq':Seq, 'totalitem':totalitem})

@login_required
def SilkC(request, data=None):
 totalitem = 0
 if data == None:
    SilkC = Colors.objects.filter(category='LF')
 elif data == 'EmbroidedVelvet' or data == 'Sequence' or data == 'tule':
    SilkC = Colors.objects.filter(category='LF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Silkcharmeuse.html', {'SilkC':SilkC, 'totalitem':totalitem})

@login_required
def FF(request, data=None):
 totalitem = 0
 if data == None:
    FF = Colors.objects.filter(category='LF')
 elif data == 'EmbroidedVelvet' or data == 'Sequence' or data == 'tule':
    FF = Colors.objects.filter(category='LF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Firefly.html', {'FF':FF, 'totalitem':totalitem})

@login_required
def MC(request, data=None):
 totalitem = 0
 if data == None:
    MC = Colors.objects.filter(category='LF')
 elif data == 'EmbroidedVelvet' or data == 'Sequence' or data == 'tule':
    MC = Colors.objects.filter(category='LF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Metallic.html', {'MC':MC, 'totalitem':totalitem})

@login_required
def Emb(request, data=None):
 totalitem = 0
 if data == None:
    Emb = Colors.objects.filter(category='LF')
 elif data == 'EmbroidedVelvet' or data == 'Sequence' or data == 'tule':
    Emb = Colors.objects.filter(category='LF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Embroidedvelvet.html', {'Emb':Emb, 'totalitem':totalitem})

def Tulle(request, data=None):
 totalitem = 0
 if data == None:
    tulle = Colors.objects.filter(category='LF')
 elif data == 'EmbroidedVelvet' or data == 'Sequence' or data == 'tulle':
    tulle = Colors.objects.filter(category='LF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Tulle.html', {'tulle':tulle, 'totalitem':totalitem})

@login_required
def BSF(request, data=None):
 totalitem = 0
 if data == None:
    Bsf = Colors.objects.filter(category='LF')
 elif data == 'EmbroidedVelvet' or data == 'Sequence' or data == 'tule':
   Bsf = Colors.objects.filter(category='LF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/BrocadeSatinFloral.html', {'Bsf':Bsf, 'totalitem':totalitem})

@login_required
def EBN(request, data=None):
 totalitem = 0
 if data == None:
    EBN = Colors.objects.filter(category='LF')
 elif data == 'EmbroidedVelvet' or data == 'Sequence' or data == 'tule':
    EBN = Colors.objects.filter(category='LF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'EmbroidedNet.html', {'EBN':EBN, 'totalitem':totalitem})

@login_required
def Muslin(request, data=None):
 totalitem = 0
 if data == None:
    muslin = Colors.objects.filter(category='LF')
 elif data == 'EmbroidedVelvet' or data == 'Sequence' or data == 'tule':
    muslin = Colors.objects.filter(category='LF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Muslin.html', {'muslin':muslin, 'totalitem':totalitem})

@login_required
def Organza(request, data=None):
 totalitem = 0
 if data == None:
    organza = Colors.objects.filter(category='LF')
 elif data == 'EmbroidedVelvet' or data == 'Sequence' or data == 'tule':
    organza = Colors.objects.filter(category='LF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Organza.html', {'organza':organza, 'totalitem':totalitem})



#def shapes(request, data=None):
#if data == None:
 #  shapes = Shapes.objects.filter(category='CF')
 #if request.user.is_authenticated:
  #      totalitem = len(Cart.objects.filter(user=request.user))
 #return render(request, 'app/shape.html', {'shapes':shapes, 'totalitem':totalitem})

@login_required
def CS(request, data=None):
 if data == None:
   cs = Colorshape.objects.filter(category='CF')
   if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/shape.html', {'cs':json_serializer.serialize(cs,ensure_ascii=False),'csdb':cs})

@login_required
def FS(request, data=None):
 if data == None:
   fs = Colorshape.objects.filter(category='FF')
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/shape1.html',{'fs':json_serializer.serialize(fs,ensure_ascii=False),'fsdb':fs})

@login_required
def LS(request, data=None):
 if data == None:
   ls = Colorshape.objects.filter(category='LF')
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/shape2.html',{'ls':json_serializer.serialize(ls,ensure_ascii=False),'lsdb':ls})

@login_required
def LN(request, data=None):
 if data == None:
   ln = Shapeneck.objects.filter(category='LF')
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Neck3.html', {'ln':json_serializer.serialize(ln,ensure_ascii=False),'lndb':ln})

#def neck(request, data=None):
 #if data == None:
  # neck = Necks.objects.filter(category='CF')
 #if request.user.is_authenticated:
  #      totalitem = len(Cart.objects.filter(user=request.user))
 #return render(request, 'app/Neckdesign.html', {'neck':neck, 'totalitem':totalitem})

def SN(request, data=None):
 if data == None:
   sn = Shapeneck.objects.filter(category='CF')
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Neckdesign.html', {'sn':json_serializer.serialize(sn,ensure_ascii=False),'sndb':sn})

def FN(request, data=None):
 if data == None:
   fn = Shapeneck.objects.filter(category='FF')
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Neck1.html', {'fn':json_serializer.serialize(fn,ensure_ascii=False),'fndb':fn})




#def sleeves(request, data=None):
 #if data == None:
  # sleeves = Sleeve.objects.filter(category='CF')
 #if request.user.is_authenticated:
   #     totalitem = len(Cart.objects.filter(user=request.user))
 #return render(request, 'app/Sleeves.html', {'sleeves':sleeves , 'totalitem':totalitem})
@login_required
def NS(request, data=None):
 if data == None:
   ns = Necksleeves.objects.filter(category='CF')
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Sleeves.html', {'ns':json_serializer.serialize(ns,ensure_ascii=False),'nsdb':ns})

@login_required
def FSL(request, data=None):
 if data == None:
   fsl = Necksleeves.objects.filter(category='FF')
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Sleeves3.html',  {'fsl':json_serializer.serialize(fsl,ensure_ascii=False),'fsldb':fsl})

def LSL(request, data=None):
 if data == None:
   lsl = Necksleeves.objects.filter(category='LF')
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Sleeves2.html',  {'lsl':json_serializer.serialize(lsl,ensure_ascii=False),'lsldb':lsl})

def Velvet(request, data=None):
 totalitem = 0
 if data == None:
    velvet = Colors.objects.filter(category='LF')
 elif data == 'Velvet' or data == 'EmbroidedLawn' or data == 'Rayon':
   velvet = Colors.objects.filter(category='LF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Velvet.html', {'velvet':velvet, 'totalitem':totalitem})

def EL(request, data=None):
 totalitem = 0
 if data == None:
    el = Colors.objects.filter(category='FF')
 elif data == 'Velvet' or data == 'EmbroidedLawn' or data == 'Rayon':
   el = Colors.objects.filter(category='FF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/EmbroidedLawn.html', {'el':el, 'totalitem':totalitem})

def Georgette(request, data=None):
 totalitem = 0
 if data == None:
    geo = Colors.objects.filter(category='FF')
 elif data == 'Velvet' or data == 'EmbroidedLawn' or data == 'Rayon':
   geo = Colors.objects.filter(category='FF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Georgette.html', {'geo':geo, 'totalitem':totalitem})

def Chiffon(request, data=None):
 totalitem = 0
 if data == None:
    chiffon = Colors.objects.filter(category='FF')
 elif data == 'Velvet' or data == 'EmbroidedLawn' or data == 'Rayon':
   chiffon = Colors.objects.filter(category='FF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Chiffon.html', {'chiffon':chiffon, 'totalitem':totalitem})

def Crinckle(request, data=None):
 totalitem = 0
 if data == None:
    crinckle = Colors.objects.filter(category='FF')
 elif data == 'Velvet' or data == 'EmbroidedLawn' or data == 'Rayon':
   crinckle = Colors.objects.filter(category='FF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Crinckled.html', {'crinckle':crinckle, 'totalitem':totalitem})

def Net(request, data=None):
 totalitem = 0
 if data == None:
    net = Colors.objects.filter(category='FF')
 elif data == 'Velvet' or data == 'EmbroidedLawn' or data == 'Rayon':
   net = Colors.objects.filter(category='FF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Net.html', {'net':net, 'totalitem':totalitem})

def CottonSilk(request, data=None):
 totalitem = 0
 if data == None:
    silk = Colors.objects.filter(category='FF')
 elif data == 'Velvet' or data == 'EmbroidedLawn' or data == 'Rayon':
   silk = Colors.objects.filter(category='FF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/CottonSilk.html', {'silk':silk, 'totalitem':totalitem})

def Crepe(request, data=None):
 totalitem = 0
 if data == None:
    crepe = Colors.objects.filter(category='FF')
 elif data == 'Velvet' or data == 'EmbroidedLawn' or data == 'Rayon':
   crepe = Colors.objects.filter(category='FF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Crepe.html', {'crepe':crepe, 'totalitem':totalitem})

def Rayon(request, data=None):
 totalitem = 0
 if data == None:
    rayon = Colors.objects.filter(category='FF')
 elif data == 'Velvet' or data == 'EmbroidedLawn' or data == 'Rayon':
   rayon = Colors.objects.filter(category='FF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Rayon.html', {'rayon':rayon, 'totalitem':totalitem})

def Khaddar(request, data=None):
 totalitem = 0
 if data == None:
    khaddar = Colors.objects.filter(category='FF')
 elif data == 'Velvet' or data == 'EmbroidedLawn' or data == 'Rayon':
   khaddar = Colors.objects.filter(category='FF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Khaddar.html', {'khaddar':khaddar, 'totalitem':totalitem})


def model(request):
  return render(request, 'app/3Dmodel.html')




def ses(request, data=None):
   
 totalitem = 0
 price = request.GET.get('price')
 if data == None:
    ses = Fabric.objects.filter(category='S')
 elif data == 'Summer' or data == 'Winter':
    ses = Fabric.objects.filter(category='S').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 if price:
   ses = Fabric.objects.filter(category='S').filter(selling_price__lte = price)
   
 return render(request, 'app/Seasons.html', {'ses':ses, 'totalitem':totalitem})

def price(request, data=None):
 totalitem = 0 
 if data == None:
   price = Fabric.objects.filter(category='S')
 elif data == '1000' or data == '4000':
   price = Fabric.objects.filter(category='S').filter(selling_price=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/pricing.html', {'price':price, 'totalitem':totalitem})
 
def Poplin(request, data=None):
 totalitem = 0
 if data == None:
    Poplin = Colors.objects.filter(category='CF')
 elif data == 'Lawn' or data == 'Printed' or data == 'Denim':
    Poplin = Colors.objects.filter(category='CF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Poplin.html', {'Poplin':Poplin, 'totalitem':totalitem})
 
def Viscose(request, data=None):
 totalitem = 0
 if data == None:
    Viscose = Colors.objects.filter(category='CF')
 elif data == 'Lawn' or data == 'Printed' or data == 'Denim':
    Viscose = Colors.objects.filter(category='CF').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Viscose.html', {'Viscose':Viscose, 'totalitem':totalitem})

def Lawn(request, data=None):
 totalitem = 0
 if data == None:
    Lawn = Colors.objects.filter(category='S')
 elif data == 'Lawn' or data == 'Printed' or data == 'Denim':
    Lawn = Colors.objects.filter(category='S').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/LawnSeason.html', {'Lawn':Lawn, 'totalitem':totalitem})

def VelvetS(request, data=None):
 totalitem = 0
 if data == None:
    VelvetS = Colors.objects.filter(category='S')
 elif data == 'Lawn' or data == 'Printed' or data == 'Denim':
    VelvetS = Colors.objects.filter(category='S').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/VelvetSeason.html', {'VelvetS':VelvetS, 'totalitem':totalitem})

@login_required
def TienDyeS(request, data=None):
 totalitem = 0
 if data == None:
    TienDyeS = Colors.objects.filter(category='S')
 elif data == 'Lawn' or data == 'Printed' or data == 'Denim':
    TienDyeS = Colors.objects.filter(category='S').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/tiendyeSeason.html', {'TienDyeS':TienDyeS, 'totalitem':totalitem})

def Printed(request, data=None):
 totalitem = 0
 if data == None:
    Printed = Colors.objects.filter(category='S')
 elif data == 'Lawn' or data == 'Printed' or data == 'Denim':
    Printed = Colors.objects.filter(category='S').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/PrintedSeason.html', {'Printed':Printed, 'totalitem':totalitem})

def Khaddar(request, data=None):
 totalitem = 0
 if data == None:
    Khaddar = Colors.objects.filter(category='S')
 elif data == 'Lawn' or data == 'Printed' or data == 'Denim':
    Khaddar = Colors.objects.filter(category='S').filter(brand=data)  
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/khaddarSeason.html', {'Khaddar':Khaddar, 'totalitem':totalitem})



def SS(request, data=None):
 if data == None:
   ss = Colorshape.objects.filter(category='S')
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/shape3.html',{'ss':json_serializer.serialize(ss,ensure_ascii=False),'ssdb':ss})


def SN(request, data=None):
 if data == None:
   sn = Shapeneck.objects.filter(category='S')
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Neck2.html', {'sn':json_serializer.serialize(sn,ensure_ascii=False),'sndb':sn})

def SSL(request, data=None):
 if data == None:
   ssl = Necksleeves.objects.filter(category='S')
 if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/Sleeves1.html', {'ssl':json_serializer.serialize(ssl,ensure_ascii=False),'ssldb':ssl})

#for payments
     
def paymentSuccess(request):
   context = {
      'payment_status':'success'
   }
   return render(request, 'app/confirmation.html', context) 

def paymentCancel(request):
   context = {
      'payment_status':'cancel'
   }
   return render(request, 'app/confirmation.html', context)  

def my_webhook_view(request):
  payload = request.body

  # For now, you only need to print out the webhook payload so you can see
  # the structure.
  print(payload)

  return HttpResponse(status=200)  

client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
def index(request):

   DATA = {
       "amount": 500000,
       "currency": "PKR",
     }
   payment_order = client.order.create(dict(data=DATA, payment_capture=1))
   payment_order_id = payment_order('id')

   context = {
      'amount': 500, 'api_key': RAZORPAY_API_KEY, 'order_id': payment_order_id
   }
   return render(request, 'pay.html', context)

 
 
def razorpaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price = total_price + item.product.selling_price * item.quantity
      
    return JsonResponse({
        'total_price': total_price
      }) 
    


def placeorder(request):
   if request.method == 'POST':
         neworder = Order()
         neworder.user = request.user
         neworder.name = request.POST.get('name')
         neworder.email = request.POST.get('email')
         neworder.phone = request.POST.get('phone')
         neworder.address = request.POST.get('address')
         neworder.country = request.POST.get('country')
         neworder.city = request.POST.get('city')
         neworder.zipcode = request.POST.get('zipcode')
         neworder.state= request.POST.get('state')
         neworder.payment_mode = request.POST.get('payment_mode')
         neworder.payment_id = request.POST.get('payment_id')
         cart = Cart.objects.filter(user = request.user)
         cart_total_price = 0
         for item in cart:
            cart_total_price = cart_total_price + item.product.selling_price * item.quantity
            
         neworder.total_price = cart_total_price
         trackno = 'salman'+ str(random.randint(1111111 , 9999999))
         while Order.objects.filter(tracking_no = trackno) is None:
              trackno = 'salman'+ str(random.randint(1111111 , 9999999))
             
         neworder.tracking_no = trackno
         neworder.save()
             
         neworderitems = Cart.objects.filter(user = request.user)
         customized_items=Cart.objects.filter(user = request.user, product__category="customized")
         print("customized_items ==> ", len(customized_items))
         for item in neworderitems:
            OrderItem.objects.create(
               order = neworder,
               product = item.product,
               price = item.product.selling_price,
               quantity = item.quantity
            )
            
         if len(customized_items) > 0:
            for customized_item in customized_items:
               items_for_recommend = Cart.objects.filter(~Q(product__category='customized'),user = request.user)
               for item in items_for_recommend:
                  [fabric_id, color_id, shape_id, neck_id, sleeve_id] = customized_item.product.attribute_ids.split('_')
                  recommendation = Recommendation()
                  recommendation.user = request.user
                  recommendation.fabric = Fabric.objects.get(id=fabric_id)
                  recommendation.color = Colors.objects.get(id=color_id)
                  if item.product.category == "Se":
                     recommendation.separate = item.product
                     is_recommedations_exist = Recommendation.objects.filter(separate=item.product.id,fabric=fabric_id,color=color_id)
                     if len(is_recommedations_exist) > 0:
                        for r in is_recommedations_exist:
                           r.separate_counter = r.separate_counter + 1
                           r.save()
                  if item.product.category == "Bm":
                     recommendation.bottom = item.product
                     is_recommedations_exist = Recommendation.objects.filter(bottom=item.product.id,fabric=fabric_id,color=color_id)
                     if len(is_recommedations_exist) > 0:
                        for r in is_recommedations_exist:
                           r.bottom_counter = r.bottom_counter + 1
                           r.save()
                  if item.product.category == "B":
                     recommendation.bag = item.product
                     is_recommedations_exist = Recommendation.objects.filter(bag=item.product.id,fabric=fabric_id,color=color_id)
                     if len(is_recommedations_exist) > 0:
                        for r in is_recommedations_exist:
                           r.bag_counter = r.bag_counter + 1
                           r.save()
                  if item.product.category == "S":
                     recommendation.shoe = item.product
                     is_recommedations_exist = Recommendation.objects.filter(shoe=item.product.id,fabric=fabric_id,color=color_id)
                     if len(is_recommedations_exist) > 0:
                        for r in is_recommedations_exist:
                           r.shoe_counter = r.shoe_counter + 1
                           r.save()
                  recommendation.save()

         Cart.objects.filter(user=request.user).delete()

         messages.success(request, "Your Order has been placed Successfully!")

         payMode = request.POST.get('payment_mode')
         if (payMode == "Paid By RazorPay" or payMode == "Paid By PayPal"):
            return JsonResponse({'status':"Your Order has been placed Successfully!"})
   return redirect('/checkout')

def orderr(request):
      #order = Order.objects.filter(user = request.user)
      #t_no = 0
      #for item in order:
       #     t_no = item.tracking_no

      #order_list = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
      #orderitems = OrderItem.objects.filter(order=order_list)
      return render(request, 'app/myorders.html')
   
   #return HttpResponse("My Orders Page")

def product(request): 
   return render(request, 'app/Product.html')
    
    

       
 