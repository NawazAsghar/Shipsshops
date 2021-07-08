from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, HttpResponseRedirect
from app.models import Product, Profile, Cart, OrderPlaced
from app.forms import RegistertionForm, ProfileForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required



def home(request):
    all_products = Product.objects.all()
    return render(request, 'app/home.html', {'products': all_products})

def product_detail(request, id):
    product = Product.objects.filter(id = id).first()
    item_in_cart = False
    if request.user.is_authenticated:
        item_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    return render(request, 'app/productdetail.html', {'product':product, 'item_in_cart':item_in_cart})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('proudct_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/showcart/')

@login_required
def show_cart(request):
    user = request.user
    carts = Cart.objects.filter(user=user)
    if not carts:
        return render(request, 'app/empty_cart.html')
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0

    cart_products = [p for p in Cart.objects.all() if p.user == user]
    if cart_products:
        for p in cart_products:
            tempamount = (p.quan * p.product.price)
            amount += tempamount
            total_amount = amount + shipping_amount

        return render(request, 'app/carts.html', {'carts':carts, 'amount':amount, 'totalamount':total_amount}) 
    else:
        return render(request, 'app/empty_cart.html')

@login_required
def pluscart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quan+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_products = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_products:
            tempamount = (p.quan * p.product.price)
            amount += tempamount
            total_amount = amount + shipping_amount 
        data = {
            'quan': c.quan,
            'amount': amount,
            'totalamount': total_amount,
        }
        return JsonResponse(data)

@login_required
def minuscart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quan -=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_products = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_products:
            tempamount = (p.quan * p.product.price)
            amount += tempamount
            total_amount = amount + shipping_amount 

        data = {
            'quan': c.quan,
            'amount': amount,
            'totalamount': total_amount,
        }

        return JsonResponse(data)

@login_required
def removecart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_products = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_products:
            tempamount = (p.quan * p.product.price)
            amount += tempamount   
        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount,
        }
        return JsonResponse(data)

###### NOT DONE ############
@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip = form.cleaned_data['zip']
            reg = Profile(user=user, name=name, address=address, city=city, state=state, zip=zip)
            reg.save()
            return HttpResponseRedirect('/profile/')
    else:
        form = ProfileForm()
    params = {'active': 'btn-primary','form':form}
    return render(request, 'app/profile.html',params)

@login_required
def address(request):
    adds = Profile.objects.filter(user = request.user.id)
    params = {'active':'btn-primary','address': adds}
    return render(request, 'app/address.html',params)

@login_required
def orders(request):
    order = OrderPlaced.objects.filter(user = request.user)
    return render(request, 'app/orders.html', {'products': order})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profile/')
    else:
        form = PasswordChangeForm(user = request.user)
    return render(request, 'app/changepassword.html', {'form':form})

def filter(request, category):
    product = Product.objects.filter(category = category)
    print(product)
    params = {'products':product}
    return render(request, 'app/filter.html', params)

def user_login(request):
    if request.method == 'POST':
        form =  AuthenticationForm(request = request, data = request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(username = uname, password = upass)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/profile/')
    else:
        form = AuthenticationForm(request= request)
    return render(request, 'app/login.html', {"form":form})

def customerregistration(request):
    if request.method == 'POST':
        form = RegistertionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')
    else: 
        form = RegistertionForm()
    return render(request, 'app/customerregistration.html', {'form':form})

@login_required
def checkout(request):
    user = request.user
    add = Profile.objects.filter(user = user)
    cart_item = Cart.objects.filter(user = user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_products = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_products:
        for p in cart_products:
            tempamount = (p.quan * p.product.price)
            amount += tempamount
        total_amount = amount + shipping_amount 
    return render(request, 'app/checkout.html', {'add':add,"cart_item":cart_item, "total_amount":total_amount})

@login_required
def paymentdone(request):
    user = request.user
    custid = request.GET.get('custid')
    profile = Profile.objects.get(id = custid)
    print(profile)
    cart = Cart.objects.filter(user =user)
    for c in cart:
        OrderPlaced(user=user, profile=profile,product=c.product, quan = c.quan).save()
        c.delete()
    return redirect('orders')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def search(request):        
    if request.method == 'GET': # this will be GET now      
        query =  request.GET.get('search') # do some research what it does       
        if query == "":
            return HttpResponseRedirect('/')
        product = Product.objects.all()
        products = []
        for p in product:
            if query in p.category.lower() or query in p.name.lower() or query in p.description.lower():
                products.append(p)
        print(products)
        return render(request,"app/search.html",{"products":products, "query":query})
    else:
        return HttpResponseRedirect('/')
