from itertools import product
from multiprocessing import context
from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import CustomerOrderForm, UserRegistrationForm, customForm
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout

from .forms import  ProductUpdateForm

from .models import Products, Category, Order, CustomerOrder,Custom

from django.contrib.auth.models import User

from django.contrib import messages

from django.db.models import Sum
from django.db.models import Q
# Create your views here.
def index(request):
    return render(request,'index.html')


def admindashboard(request):
    return render(request,'admindashboard.html')             

def contactus(request):
    return render(request,'contactus.html')             


def customerdashboard(request):
    return render(request,'customerdashboard.html')

def signin(request):
    form = AuthenticationForm()
    if request.method =="POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'])
            login(request, user)
            print(user.is_superuser)
            if user.is_superuser == True:
                return redirect('/admindashboard/')
            else: 
                return redirect('/customerdashboard/')
    return render(request, 'signin.html', {'form': form})

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            #return HttpRespone('Done')
            return redirect('/signin/')

    else:
            form = UserRegistrationForm()   

    context = {
        'form': form
    }             

    return render(request, 'signup.html', context)

def signout(request):
        logout(request)
        return redirect('/index/')   


@login_required(login_url='signin')
def welcome(request):
    products = Products.objects.all()
    products_count = Products.objects.all().count()
    total_orders = CustomerOrder.objects.all().count()

    orders_delivered = CustomerOrder.objects.filter(status=True).count()
    orders_pending = CustomerOrder.objects.filter(status=False).count()

    customers = User.objects.all().count()

    customer_orders = CustomerOrder.objects.filter(customer=request.user).filter(status=True).count()

 

    customer_orders1 = Order.objects.filter(customer=request.user).count()

    context = {
        'products': products,
        'products_count': products_count,
        'total_orders': total_orders,
        'orders_delivered': orders_delivered,
        'orders_pending': orders_pending,
        'customers': customers,

        'customer_orders': customer_orders,
        'customer_orders1': customer_orders1,
     


    }
    return render(request, 'welcome.html', context)

def all_customers(request):
    customers = User.objects.all()
    context = {
        'customers': customers
    }
    return render(request, 'customers.html', context)

def view_customer(request, pk):
    customer = User.objects.get(id=pk)


    context = {
        'customer': customer

    }

    return render(request, 'view_customer.html', context)


def all_products(request):
    category =  request.GET.get('category')
    if category == None:
        products = Products.objects.all()
    else:
        products = Products.objects.filter(category__name=category)
        
    categories = Category.objects.all()

    user = request.user

    if user.is_authenticated:
        cart = Order.objects.filter(customer=user).count()
    else:
        cart = ''


    context = {
        'products': products,
        'categories': categories,
        'cart': cart
    }

    return render(request, 'products.html', context)

    


def view_product(request, pk):
    product = Products.objects.get(id=pk)

    context = {
        'product': product
    }

    return render(request, 'view_product.html', context)

def update_product(request, pk):
    product = Products.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    
    else:
        form = ProductUpdateForm(instance=product)

    context = {
        'form': form
    }

    return render(request, 'productupdate.html', context)
    

def add_product(request):
    
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])

        else:
             category = None

        products = Products.objects.create(
            category = category,
            image = image, 
            name = data['name'],
            price = data['price'],
            description = data['description'],
        )

        return redirect('products')

        
    context = {
        'categories': categories,
    }
    return render(request, 'addproduct.html', context)

def custom(request):
    form = customForm()
    if request.method == 'POST':
        form = customForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/customerdashboard')
    
    else:
        form = customForm()
    context = {
        'form': form
    }  

    return render(request,'uploadfile.html', context)



def order_list(request):
    orders = CustomerOrder.objects.all()

    context = {
        'orders': orders
    }
    return render(request, 'orders.html', context)



def add_to_cart(request, pk):

    user = request.user
    order_product = Products.objects.get(id=pk)

    if request.user.is_authenticated:
        if Order.objects.filter(customer = user, product=pk).exists():
            # return HttpResponse('This item is already on the cart')
            messages.success(request, 'This item is already on the cart')
            return redirect('products')

        else:
            Order.objects.create(customer = user, product = order_product, order_quantity=1)
            
            CustomerOrder.objects.create(customer = user, product = order_product, order_quantity=1)

            
            return redirect('products')
    else:
        return HttpResponse('Please login first')

def checkout(request):
    if request.method == 'POST':
        address = request.POST['address']
        phone = request.POST['phone']

        order = Order.objects.filter(customer = request.user).all()
        order.delete()


        order = CustomerOrder.objects.filter(customer = request.user).update(
            address = address,
            phone = phone
        )
        
        # context = {
        #     'cart_items': None
        # }

    
        # return render(request, 'cart_item.html', context)
        return redirect('cart_items')

        
def cart_items(request):

    user = request.user
    total = Order.objects.filter(customer=user).aggregate(thedata=Sum('total_price'))


    if request.user.is_authenticated:
        cart_items = Order.objects.filter(customer=user).all()

    else:
        cart_items = ''
    
    context = {
        'cart_items': cart_items,
        'total': total
    }

    return render(request, 'cart_item.html', context)

def add_quantity(request, pk):

    quantity_cart = Order.objects.get(id=pk)

    hello = CustomerOrder.objects.get(id = pk)

    hello.order_quantity += 1

    hello.save()


    quantity_cart.order_quantity += 1
    
    quantity_cart.save()

    return redirect('cart_items')



def sub_quantity(request, pk):
    quantity_cart = Order.objects.get(id=pk)

    hello = CustomerOrder.objects.get(id = pk)

    hello.order_quantity -= 1

    hello.save()

    if hello.order_quantity == 0:
        hello.delete()



    # print(quantity)
    quantity_cart.order_quantity -= 1

    quantity_cart.save()


    if quantity_cart.order_quantity == 0:
        quantity_cart.delete()


    return redirect('cart_items')
    


def customer_orders(request):
    orders = CustomerOrder.objects.filter(customer=request.user).all()

    context = {
        'orders': orders
    }
    return render(request, 'customer_orders.html', context)


def cancel_order(request, pk):
    cancel_cart = Order.objects.get(id=pk)

    hello = CustomerOrder.objects.get(id=pk)

    hello.delete()

    cancel_cart.delete()

    return redirect('cart_items')

def all_orders(request, pk):
    order = CustomerOrder.objects.get(id=pk)
    if request.method == 'POST':
        order_form = CustomerOrderForm(request.POST, instance=order)
        if order_form.is_valid():
            order_form.save()
            return redirect('order')
    
    else:
        order_form = CustomerOrderForm(instance=order)

    context = {
        'order_form': order_form
    }

    return render(request, 'update_orders.html', context)








def search(request):
    search_post = request.GET.get('search')
    if search_post:
        search = Products.objects.filter(Q(name__icontains=search_post))
    else:
        return HttpResponse('Sorry No match Found')

    categories = Category.objects.all()

    context = {
        'search': search,
        'categories': categories,
    }

    return render(request, 'search.html', context)

def delete_product(request, pk):
    delete_product = Products.objects.get(id=pk)

    delete_product.delete()

    return redirect('products')

def khalti(request):
    
    return redirect('products')

def custom_orders(request):
    orders = Custom.objects.all()

    context = {
        'orders': orders
    }
    return render(request, 'custom_order.html', context)
