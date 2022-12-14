from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from app.models import Order
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    path('', views.ProductView.as_view(), name="home"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('bags/', views.bags, name='bags'),
    path('bags/<slug:data>', views.bags, name='bagsdata'),
    path('shoes/', views.shoes, name='shoes'),
    path('shoes/<slug:data>', views.shoes, name='shoesdata'),
    path('bottoms/', views.bottoms, name='bottoms'),
    path('bottoms/<slug:data>', views.bottoms, name='bottomsdata'),
    path('seperates/', views.seperates, name='seperates'),
    path('seperates/<slug:data>', views.seperates, name='seperatesdata'),
    path('checkout/', views.checkout, name='checkout'),
    #path('paymentdone/', views.payment_done, name='paymentdone'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', 
    authentication_form=LoginForm), name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', 
    form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', 
    form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), 
    name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', 
    form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), 
    name='password_reset_complete'),
    path('registration/', views.CustomerRegistrationView.as_view(), name="customerregistration"),
    path('CasualFabric/', views.Casual, name="CasualFabric"),
    path('CasualFabric/<slug:data>', views.Casual, name="CasualFabricdata"),
    path('FestiveFabric/', views.Festive, name="FestiveFabric"),
    path('FestiveFabric/<slug:data>', views.Festive, name="FestiveFabricdata"),
    path('LuxuryFabric/', views.Luxury, name="LuxuryFabric"),
    path('LuxuryFabric/<slug:data>', views.Luxury, name="LuxuryFabricdata"),
    path('Lawn/', views.CFC, name='Lawn'),
    path('Lawn/<slug:data>', views.CFC, name='Lawndata'),
    path('Color/', views.CFC, name='Color'),
    path('Color/<slug:data>', views.CFC, name='Colordata'),
    path('Printed/', views.PFC, name='Printed'),
    path('Printed/<slug:data>', views.PFC, name='Printeddata'),
    path('Denim/', views.Denim, name='Denim'),
    path('Denim/<slug:data>', views.Denim, name='Denimdata'),
    path('TieDye/', views.TienDye, name='TieDye'),
    path('TieDye/<slug:data>', views.TienDye, name='TieDyemdata'),
    path('Floral/', views.floral, name='Floral'),
    path('Floral/<slug:data>', views.floral, name='Floraldata'),
    path('silk/', views.Silk, name='silk'),
    path('silk/<slug:data>', views.Silk, name='silkdata'),
    path('Cambric/', views.Cambric, name='Cambric'),
    path('Cambric/<slug:data>', views.Cambric, name='Cambricdata'),
    path('Nylon/', views.Nylon, name='Nylon'),
    path('Nylon/<slug:data>', views.Nylon, name='Nylondata'),
    path('Linen/', views.Linen, name='Linen'),
    path('Linen/<slug:data>', views.Linen, name='Linendata'),
    path('Canva/', views.Canva, name='Canva'),
    path('Canva/<slug:data>', views.Canva, name='Canvadata'),
    path('RayonC/', views.RayonC, name='RayonC'),
    path('RayonC/<slug:data>', views.RayonC, name='RayonCdata'),
    path('Embvelvet/', views.Embroidedvelvet, name='Embvelvet'),
    path('Embvelvet/<slug:data>', views.Embroidedvelvet, name='Embvelvetdata'),
    path('sequence/', views.Seq, name='sequence'),
    path('sequence/<slug:data>', views.Seq, name='sequencedata'),
    path('Silkcharmeuse/', views.SilkC, name='Silkcharmeuse'),
    path('Silkcharmeuse/<slug:data>', views.SilkC, name='Silkcharmeusedata'),
    path('Tulle/', views.Tulle, name='Tulle'),
    path('Tulle/<slug:data>', views.Tulle, name='Tulledata'),
    path('Firefly/', views.FF, name='Firefly'),
    path('Firefly/<slug:data>', views.FF, name='Firefly'),
    path('Metallic/', views.MC, name='Metallic'),
    path('Metallic/<slug:data>', views.MC, name='Metallic'),
    path('Embroidedvelvet/', views.Emb, name='Embroidedvelvet'),
    path('Embroidedvelvet/<slug:data>', views.Emb, name='Embroidedvelvetdata'),
    path('BrocadeSatinFloral/', views.BSF, name='BrocadeSatinFloral'),
    path('BrocadeSatinFloral/<slug:data>', views.BSF, name='BrocadeSatinFloral'),
    path('EmbroidedNet/', views.EBN, name='EmbroidedNet'),
    path('EmbroidedNet/<slug:data>', views.EBN, name='EmbroidedNetdata'),
    path('shape/', views.CS, name='shape'),
    path('shape/<slug:data>', views.CS, name='shapedata'),
    path('shape1/', views.FS, name='shape1'),
    path('shape1/<slug:data>', views.FS, name='shape1data'),
    path('shape2/', views.LS, name='shape2'),
    path('shape2/<slug:data>', views.LS, name='shape2data'),
    path('Neckdesign/', views.SN, name='Neckdesign'),
    path('Neckdesign/<slug:data>', views.SN, name='Neckdesigndata'),
    path('Neck1/', views.FN, name='Neck1'),
    path('Neck1/<slug:data>', views.FN, name='Neck1data'),
    path('Neck3/', views.LN, name='Neck3'),
    path('Neck3/<slug:data>', views.LN, name='Neck3data'),
    path('Sleeves/', views.NS, name='Sleeves'),
    path('Sleeves/<slug:data>', views.NS, name='Sleevesdata'),
    path('Sleeves2/', views.LSL, name='Sleeves2'),
    path('Sleeves2/<slug:data>', views.FSL, name='Sleeves3data'),
    path('Sleeves3/', views.FSL, name='Sleeves3'),
    path('Sleeves3/<slug:data>', views.LSL, name='Sleeves3data'),
    path('Velvet/', views.Velvet, name='Velvet'),
    path('Velvet/<slug:data>', views.Velvet, name='Velvetdata'),
    path('EmbroidedLawn/', views.EL, name='EmbroidedLawn'),
    path('EmbroidedLawn/<slug:data>', views.EL, name='EmbroidedLawndata'),
    path('Georgette/', views.Georgette, name='Georgette'),
    path('Georgette/<slug:data>', views.Georgette, name='Georgettedata'),
    path('Chiffon/', views.Chiffon, name='Chiffon'),
    path('Chiffon/<slug:data>', views.Chiffon, name='Chiffondata'),
    path('Crinckled/', views.Crinckle, name='Crinckled'),
    path('Crinckled/<slug:data>', views.Crinckle, name='Crinckleddata'),
    path('Net/', views.Net, name='Net'),
    path('Net/<slug:data>', views.Net, name='Netdata'),
    path('CottonSilk/', views.CottonSilk, name='CottonSilk'),
    path('CottonSilk/<slug:data>', views.CottonSilk, name='CottonSilkdata'),
    path('Crepe/', views.Crepe, name='Crepe'),
    path('Net/<slug:data>', views.Crepe, name='Crepedata'),
    path('Rayon/', views.Rayon, name='Rayon'),
    path('Rayon/<slug:data>', views.Rayon, name='Rayondata'),
    path('Khaddar/', views.Khaddar, name='Khaddar'),
    path('Khaddar/<slug:data>', views.Khaddar, name='Khaddardata'),
    path('Muslin/', views.Muslin, name='Muslin'),
    path('Muslin/<slug:data>', views.Muslin, name='Muslindata'),
    path('Organza/', views.Organza, name='Organza'),
    path('Organza/<slug:data>', views.Organza, name='Organzadata'),
    path('3Dmodel/', views.model, name='3Dmodel'),
    path('Seasons/', views.ses , name='Seasons'),
    path('Seasons/<slug:data>', views.ses, name='Seasonsdata'),
    path('Poplin/', views.Poplin, name='Poplin'),
    path('Poplin/<slug:data>', views.Poplin, name='Poplindata'),
    path('Viscose/', views.Viscose, name='Viscose'),
    path('Viscose/<slug:data>', views.Viscose, name='Viscosedata'),
    path('LawnSeaon/', views.Lawn, name='LawnSeason'),
    path('LawnSeason/<slug:data>', views.Lawn, name='LawnSeasondata'),
    path('khaddarSeason/', views.Khaddar, name='khaddarSeason'),
    path('khaddarSeason/<slug:data>', views.Khaddar, name='khaddarSeasondata'),
    path('shape3/', views.SS, name='shape3'),
    path('shape3/<slug:data>', views.SS, name='shape3data'),
    path('VelvetSeaon/', views.VelvetS, name='VelvetSeason'),
    path('VelvetSeason/<slug:data>', views.VelvetS, name='VelvetSeasondata'),
    path('PrintedSeaon/', views.Printed, name='PrintedSeason'),
    path('PrintedSeason/<slug:data>', views.Printed, name='PrintedSeasondata'),
    path('tiendyeSeason/', views.TienDyeS, name='tiendyeSeason'),
    path('tiendyeSeason/<slug:data>', views.TienDyeS, name='tiendyeSeasondata'),
    path('Neck2/', views.SN, name='Neck2'),
    path('Neck2/<slug:data>', views.SN, name='Neck2data'),
    path('Sleeves1/', views.SSL, name='Sleeves1'),
    path('Sleeves1/<slug:data>', views.SSL, name='Sleeves1data'),
    path('payment-success/', views.paymentSuccess, name='payment-success'),
    path('payment-cancel/', views.paymentCancel, name='payment-cancel'),
    path('webhook/stripe', views.my_webhook_view, name='webhook-stripe'),
    path('pay/', views.index, name='pay'),
    #path('detail/', views.details, name='detail'),
    path('Product/', views.product, name='Product'),
    path('proceed-to-pay', views.razorpaycheck ),
    path('place-order', views.placeorder , name="placeorder"),
    path('my-orders', views.orderr),
    path('myorders', views.orderr, name='myorders')
#path('Lawn/<int:ck>', views.ColorView.as_view(), name='Lawn')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)