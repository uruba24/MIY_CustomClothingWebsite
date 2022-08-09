from django.contrib import admin
from .models import(
    Customer,
    Product,
    OrderPlaced,
    Fabric,
    Colors,
    Shapes,
    Colorshape,
    Necks,
    Shapeneck,
    Sleeve,
    Necksleeves,
    Bottoms,
    Order,
    OrderItem,
    Cart,
    Basket,
    Budget,
    Recommendation
)
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display= ['id','user','name','locality','city','zipcode','state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
     list_display= ['id','title','selling_price','discounted_price','description','brand','category','product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
     list_display= ['id','user','product','quantity']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
     list_display= ['id','user','customer','product','quantity','ordered_date','status']

@admin.register(Fabric)
class FabricModelAdmin(admin.ModelAdmin):
     list_display= ['id','title','selling_price','discounted_price','brand','category','product_image']

@admin.register(Colors)
class ColorModelAdmin(admin.ModelAdmin):
     list_display= ['id','fk','category','price','brand','product_image']

@admin.register(Shapes)
class ShapesModelAdmin(admin.ModelAdmin):
     list_display= ['id','fabric_fk','color_fk','title','price','category','product_image']
     
@admin.register(Colorshape)
class ColorshapeModelAdmin(admin.ModelAdmin):
     list_display= ['id','color_fk','shape_fk','category','price','product_image']     
     
@admin.register(Necks)
class NecksModelAdmin(admin.ModelAdmin):
     list_display= ['id','title','price','category','product_image']
     
@admin.register(Shapeneck)
class ShapeneckModelAdmin(admin.ModelAdmin):
     list_display= ['id','colorshape_fk','neck_fk','category','price','product_image']                  

@admin.register(Sleeve)
class SleeveModelAdmin(admin.ModelAdmin):
     list_display= ['id','title','price','category','product_image']

@admin.register(Necksleeves)
class NeckSleevesModelAdmin(admin.ModelAdmin):
     list_display= ['id','shapeneck_fk','sleeve_fk','category','price','product_image']   

@admin.register(Bottoms)
class BottomsModelAdmin(admin.ModelAdmin):
     list_display= ['id','title','price','category','product_image']

@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
     list_display= ['id','user','name','email','phone','address','country','city','zipcode','state','total_price','payment_mode','payment_id','status','message','tracking_no','created_at','updated_at']              
# Register your models here.
@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
     list_display= ['id','order','product','price','quantity']
     
@admin.register(Basket)
class BasketModelAdmin(admin.ModelAdmin):
     list_display= ['id','user','product','quantity']     
     
@admin.register(Budget)
class BudgetModelAdmin(admin.ModelAdmin):
     list_display= ['id','user','price']   
     
@admin.register(Recommendation)
class RecommendationModelAdmin(admin.ModelAdmin):
     list_display= ['id','user','budget', 'fabric', 'color', 'shape', 'neck', 'sleeve', 'bag', 'shoe', 'bottom', 'separate']      
     
