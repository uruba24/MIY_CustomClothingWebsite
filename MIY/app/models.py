from email import message
from importlib import machinery
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

STATE_CHOICES = (
    ('Andaman & Nicobar Islands','Andaman & Nicobar'),
    ('Andhra Pradesh','Andhra Pardesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chhatisgarh','Chhatisgarh'),
    ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),

)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

def __str__(self):
        return str(self.id)

CATEGORY_CHOICES = (
            ('Se', 'Seperates'),
            ('Bm', 'Bottom'),
            ('B', 'Bags'),
            ('S', 'Shoes')
            )
class Product(models.Model):
            title = models.CharField(max_length=100)
            selling_price = models.FloatField()
            discounted_price = models.FloatField()
            description = models.TextField()
            brand = models.CharField(max_length=200)
            category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
            product_image = models.ImageField(upload_to='productimg')
            attribute_ids = models.CharField(max_length=200, null=True, blank=True)

def __str__(self):
    return str(self.id)

class Cart(models.Model):
                    user = models.ForeignKey(User, on_delete=models.CASCADE)
                    product = models.ForeignKey(Product, on_delete=models.CASCADE)
                    quantity = models.PositiveIntegerField(default=1)

def __str__(self):
    return str(self.id)

@property
def total_cost(self):
  return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
                            ('Accepted','Accepted'),
                            ('Packed','Packed'),
                            ('On The Way','On The Way'),
                            ('Delivered','Delivered'),
                            ('Cancel','Cancel')
                        )

class OrderPlaced(models.Model):
                            user = models.ForeignKey(User, on_delete=models.CASCADE)
                            customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
                            product = models.ForeignKey(Product, on_delete=models.CASCADE)
                            quantity = models.PositiveIntegerField(default=1)
                            ordered_date = models.DateTimeField('edit date ', auto_now=True)
                            status = models.CharField(max_length=50, choices=STATUS_CHOICES,default='Pending')


@property
def total_cost(self):
  return self.quantity * self.product.discounted_price      

FABRIC_CHOICES = (
    ('CF', 'CasualFabric'),
    ('FF', 'FestiveFabric'),
    ('LF', 'LuxuryFabric'),
    ('S', 'Seasons')
  

)
class Fabric(models.Model):
            title = models.CharField(max_length=100)
            selling_price = models.FloatField()
            discounted_price = models.FloatField()
            brand = models.CharField(max_length=200)
            category = models.CharField(choices=FABRIC_CHOICES,max_length=2)
            product_image = models.ImageField(upload_to='productimg')

def __str__(self):
    return str(self.id)

COLOR_CHOICES = (
    ('CF', 'CasualFabric'),
    ('FF', 'FestiveFabric'),
    ('LF', 'LuxuryFabric')
)
class Colors(models.Model):
            fk = models.ForeignKey(Fabric,on_delete=models.DO_NOTHING)
            category = models.CharField(choices=FABRIC_CHOICES,max_length=2)
            price = models.FloatField()
            brand = models.CharField(max_length=200)
            product_image = models.ImageField(upload_to='productimg')

def __str__(self):
    return str(self.id)

class Shapes(models.Model):
          fabric_fk = models.ForeignKey(Fabric,on_delete=models.CASCADE)
          color_fk = models.ForeignKey(Colors,on_delete=models.CASCADE)
          title = models.CharField(max_length=100)
          price = models.FloatField()
          category = models.CharField(choices=FABRIC_CHOICES,max_length=2)
          product_image = models.ImageField(upload_to='productimg')

def __str__(self):
        return str(self.id)
    
class Colorshape(models.Model):
          color_fk = models.ForeignKey(Colors,on_delete=models.CASCADE)
          shape_fk = models.ForeignKey(Shapes,on_delete=models.CASCADE)
          category = models.CharField(choices=FABRIC_CHOICES,max_length=2)
          price = models.FloatField()
          product_image = models.ImageField(upload_to='productimg') 
          
def __str__(self):
        return str(self.id)                      

class Necks(models.Model):
          title = models.CharField(max_length=100)
          price = models.FloatField()
          category = models.CharField(choices=FABRIC_CHOICES,max_length=2)
          product_image = models.ImageField(upload_to='productimg')

def __str__(self):
        return str(self.id)
    
class Shapeneck(models.Model):
          colorshape_fk = models.ForeignKey(Colorshape,on_delete=models.CASCADE)
          neck_fk = models.ForeignKey(Necks,on_delete=models.CASCADE)
          category = models.CharField(choices=FABRIC_CHOICES,max_length=2)
          price = models.FloatField()
          product_image = models.ImageField(upload_to='productimg')
          
def __str__(self):
        return str(self.id) 
    
class Sleeve(models.Model):
          title = models.CharField(max_length=100)
          price = models.FloatField()
          category = models.CharField(choices=FABRIC_CHOICES,max_length=2)
          product_image = models.ImageField(upload_to='productimg') 
          
class Necksleeves(models.Model):
          shapeneck_fk = models.ForeignKey(Shapeneck,on_delete=models.CASCADE)
          sleeve_fk = models.ForeignKey(Sleeve,on_delete=models.CASCADE)
          category = models.CharField(choices=FABRIC_CHOICES,max_length=2)
          price = models.FloatField()
          product_image = models.ImageField(upload_to='productimg')
          
def __str__(self):
        return str(self.id) 
          

class Bottoms(models.Model):
          title = models.CharField(max_length=100)
          price = models.FloatField()
          category = models.CharField(choices=FABRIC_CHOICES,max_length=2)
          product_image = models.ImageField(upload_to='productimg')       
          
          
class Order(models.Model): 
          user = models.ForeignKey(User, on_delete=models.CASCADE)   
          name = models.CharField(max_length=150, null=False)                  
          email = models.CharField(max_length=150, null=False) 
          phone = models.CharField(max_length=150, null=False) 
          address = models.TextField(null=False) 
          country = models.CharField(max_length=150, null=False) 
          city = models.CharField(max_length=150, null=False) 
          zipcode = models.CharField(max_length=150, null=False) 
          state = models.CharField(max_length=150, null=False) 
          total_price = models.FloatField(null = False)
          payment_mode = models.CharField(max_length=150 , null=False)
          payment_id = models.CharField(max_length=250 , null=True)
          orderstatuses = (
                            ('Pending','Pending'),
                            ('On The Way','On The Way'),
                            ('Delivered','Delivered'),
                            ('Cancel','Cancel')
          )
      
          status = models.CharField(max_length=150 , choices=orderstatuses, default='Pending')
          message = models.TextField(null=True)
          tracking_no = models.CharField(max_length=150 , null = True)
          created_at = models.DateTimeField(auto_now_add=True)
          updated_at = models.DateTimeField(auto_now=True)
          
def __str__(self):
        return '{} - {}'.format(self.id , self.tracking_no) 
          
class OrderItem(models.Model): 
     order = models.ForeignKey(Order, on_delete=models.CASCADE) 
     product = models.ForeignKey(Product, on_delete=models.CASCADE)      
     price = models.FloatField(null=False)
     quantity = models.IntegerField(null=False)
     
     
def __str__(self):
        return '{} - {}'.format(self.order.id , self.order.tracking_no) 
    
    
class Basket(models.Model):
                    user = models.ForeignKey(User, on_delete=models.CASCADE)
                    product = models.ForeignKey(Necksleeves, on_delete=models.CASCADE)
                    quantity = models.PositiveIntegerField(default=1)

def __str__(self):
    return str(self.id)  

class Budget(models.Model):
                    user = models.ForeignKey(User, on_delete=models.CASCADE)
                    price = models.FloatField(null=False)

def __str__(self):
    return str(self.id)  

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, null=True, blank=True)
    fabric = models.ForeignKey(Fabric,on_delete=models.DO_NOTHING, null=True, blank=True)
    color = models.ForeignKey(Colors,on_delete=models.CASCADE, null=True, blank=True)
    shape = models.ForeignKey(Colorshape,on_delete=models.CASCADE, null=True, blank=True)
    neck = models.ForeignKey(Shapeneck,on_delete=models.CASCADE, null=True, blank=True)
    sleeve = models.ForeignKey(Necksleeves,on_delete=models.CASCADE, null=True, blank=True)
    bag = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bag', null=True, blank=True)
    shoe = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='shoe', null=True, blank=True)
    bottom = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bottom', null=True, blank=True)
    separate = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='separate', null=True, blank=True)
    bag_counter=models.IntegerField(default=1,null=True,blank=True)
    shoe_counter=models.IntegerField(default=1,null=True,blank=True)
    separate_counter=models.IntegerField(default=1,null=True,blank=True)
    bottom_counter=models.IntegerField(default=1,null=True,blank=True)
    
def __str__(self):
    return str(self.id)
    



