from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

## For image handeling
from django.conf import settings
from django.conf.urls.static import static


urlpatterns= [
    path('',views.index),
    path('index/',views.index),
    path('signin/', views.signin, name="User Sign In"),
    path('contactus/', views.contactus, name="Contacts"),
    path('signup/', views.registration, name="User Sign Up"),
    path('signout/', views.signout, name="User Sign Out"),
    path('admindashboard/', views.admindashboard, name="Admin dashboard"),
    path('customerdashboard/', views.customerdashboard, name="Customer dashboard"),
    path('products/', views.all_products, name='products'),
     path('welcome/', views.welcome, name='welcome'),


    path('products/<str:pk>', views.view_product, name='view_product'),

    path('addproducts/', views.add_product, name='add_product'),
     path('uploadfile/', views.custom, name='custom'),

    path('updateproduct/<str:pk>', views.update_product, name='update_product'),

    path('search/', views.search, name='search'),

    path('order/', views.order_list, name='order'),

    path('cart/<str:pk>', views.add_to_cart, name='cart'),

    path('cartitem/', views.cart_items, name='cart_items'),


    path('customerorder/', views.customer_orders, name='customer_order'),

     path('custom_order/', views.custom_orders, name='custom_order'),

    path('checkout/', views.checkout, name='checkout'),


    path('addquantity/<str:pk>', views.add_quantity, name='addquantity'),

    path('subquantity/<str:pk>', views.sub_quantity, name='subquantity'),

    path('cancel_order/<str:pk>', views.cancel_order, name='cancel_order'),

    path('checkout/', views.checkout, name='checkout'),

    path('customers/', views.all_customers, name='customers'),

    path('customer/<str:pk>', views.view_customer, name='view_customer'),

    path('allorders/<str:pk>', views.all_orders, name='all_orders'),

    path('delete_product/<str:pk>', views.delete_product, name='delete_product'),                    

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)