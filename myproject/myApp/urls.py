from . import views
from django.urls import path

urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register,name='register'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logout_page,name='logout'),
    path('cart/',views.cart_page,name='cart'),
    path('fav',views.fav_page,name='fav'),
    path('favviewpage',views.favviewpage,name='favviewpage'),
    path('remove_cart/<str:cid>',views.remove_cart,name='remove_cart'),
    path('remove_fav/<str:cid>',views.remove_fav,name='remove_fav'),
    path('collections/',views.collections,name='collections'),
    path('collections/<str:name>/',views.collectionview,name='collectionview'),
    path('collections/<str:cname>/<str:pname>/',views.Product_details,name='Product_details'),
    path('addtocart',views.add_to_cart,name='addtocart'),

]
