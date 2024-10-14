from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout
from pathlib import Path
import os

def home(request):
    products = []
    for product in Product.objects.all().order_by('-id'):
        products.append([product, [size.size for size in product.sizes.all()]])
    context = {
        'title': Title.objects.first(),
        'first_image' : Slide.objects.all().first(),
        'rest_images' : Slide.objects.exclude(id = Slide.objects.all().first().id).order_by('id'),
        'categories' : Category.objects.all(),
        'products' : products,
    }
    return render(request, 'pages/home.html', context)

def cart(request):
    cart = request.session.get('cart', {})
    context = {
        'cart' : cart,
    }
    if cart:
        products = []
        for key in cart.keys():
            product_id, size = key.split('_')
            if Product.objects.filter(id = product_id).exists():
                product = Product.objects.get(id = product_id)
                products.append([product, size, cart[key], key])
        context.update({
            'products' : products,
        })
    return render(request, 'pages/cart.html', context)

@csrf_exempt
def add_cart(request):
    cart = request.session.get('cart', {})
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        print('S' in Product.objects.get(id = product_id).sizes.all())
        size = request.POST.get('size')
        product_key = f'{product_id}_{size}'
        if product_key in cart.keys():
            cart[product_key] = int(cart.get(product_key)) + 1
            request.session['cart'] = cart
            print(cart.get(product_key))
        else:
            cart[product_key] = 1
            request.session['cart'] = cart
            print(cart.get(product_key))
        return JsonResponse({
            'status' : 'Added to Cart',
            'product_quantity' : cart[product_key],
        })

@csrf_exempt
def update_cart(request):
    cart = request.session.get('cart', {})
    if request.method == "POST":
        product_key = request.POST.get('product_key')
        new_quantity = request.POST.get('quantity')
        cart[product_key] = new_quantity
        request.session['cart'] = cart
        return JsonResponse({
            'status' : 'updated',
        })

@csrf_exempt
def remove_product(request):
    cart = request.session.get('cart', {})
    if request.method == "POST":
        product_key = request.POST.get('product_key')
        cart.pop(product_key)
        print(cart)
        request.session['cart'] = cart
        return JsonResponse({
            'status' : 'product removed'
        })

def checkout(request):
    cart = request.session.get('cart', {})
    if request.method == 'POST':
        # For Order Items
        order_items = []
        for key, value in cart.items():
            product_id, size = key.split('_')
            quantity = value
            order_items.append(OrderItem.objects.create(
                        product = Product.objects.get(id = product_id),
                        total = Product.objects.get(id = product_id).price * int(quantity),
                        size = size,
                        quantity = quantity,
            ))
        # For Order-Form
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        wilaya = request.POST.get('wilaya')
        shipping = request.POST.get('shipping')
        if shipping:
            if shipping == 'Yalidine':
                maktab = request.POST.get('maktab')
                new_order = Order.objects.create(
                    full_name = full_name,
                    phone_number = phone_number,
                    delivery = shipping,
                    wilaya = wilaya,
                    desktop = maktab,
                )
                order_subtotal = 0
                for order_item in order_items:
                    order_subtotal += order_item.total
                for order_item in order_items:
                    
                    new_order.order_items.add(order_item)
                    new_order.total = order_subtotal + Wilaya.objects.get(name = wilaya).yalidine_price
                new_order.save()
                request.session['cart'] = {}
                request.session.modified = True
                messages.success(request, 'Order is successfully send !')
                return redirect('home')
            else:
                township = request.POST.get('township')
                adress = request.POST.get('adress')
                new_order = Order.objects.create(
                    full_name = full_name,
                    phone_number = phone_number,
                    delivery = shipping,
                    wilaya = wilaya,
                    township = township,
                    adress = adress,
                )
                order_subtotal = 0
                for order_item in order_items:
                    order_subtotal += order_item.total
                for order_item in order_items:
                    
                    new_order.order_items.add(order_item)
                    new_order.total = order_subtotal + Wilaya.objects.get(name = wilaya).domicile_price
                new_order.save()
                request.session['cart'] = {}
                request.session.modified = True
                messages.success(request, 'Order is successfully send !')
                return redirect('home')

    
    products = []
    subtotal = 0
    for key, value in cart.items():
        product_id, size = key.split('_')
        quantity = value
        products.append([Product.objects.get(id = product_id), size, quantity, (int(quantity) * Product.objects.get(id = product_id).price)])
        subtotal += (int(quantity) * Product.objects.get(id = product_id).price)
    context = {
        'products' : products,
        'subtotal' : subtotal,
    }
    return render(request, 'pages/checkout.html', context)

@csrf_exempt
def update_wilaya(request):
    if request.method == "POST":
        wilaya_name = request.POST.get('wilaya_name')
        wilaya = Wilaya.objects.get(name = wilaya_name)
        makatib = list(wilaya.maktab.values('name'))
        return JsonResponse({
            'status' : 'changed',
            'yalidine_price' : wilaya.yalidine_price,
            'domicile_price' : wilaya.domicile_price,
            'makatib' : makatib,
        })

def login_page(request):
    if request.method == "POST":
        user_form = UserLoginForm(data = request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password')
            admin = authenticate(username = username, password = password)
            if admin is not None:
                login(request, admin)
                messages.success(request, 'Login Successfully')
                return redirect('home')
            else:
                messages.error(request, 'Your Login Failed !')
                return redirect('home')
        else:
            messages.error(request, 'Your Login Failed !')
            return redirect('home')
                
    context = {
        'UserLoginForm' : UserLoginForm(),
    }
    return render(request, 'pages/login.html', context)

def logout_page(request):
    logout(request)
    return redirect('home')

def control(request):
    context = {
        
    }
    return render(request, 'pages/control.html', context)

def edit_main_interface(request):
    current_title = Title.objects.first()
    if request.method == 'POST':
        new_title = TitleForm(request.POST, instance = current_title)
        new_slides = request.FILES.getlist('slide')
        new_slides.reverse()
        if new_title.is_valid() and ( len(new_slides) > 1 ):
            new_title.save()
            slides = Slide.objects.all()
            for old_slide in slides:
                old_image_slide = old_slide.image.path
                if os.path.exists(old_image_slide):
                    os.remove(old_image_slide)
                old_slide.delete()
            
            for new_slide in new_slides:
                Slide.objects.create(image = new_slide)
            messages.success(request, 'Main interface is succefully Edited !')
            return redirect('home')
        elif(new_title.is_valid()):
            new_title.save()
            messages.success(request, 'Title is succefully Edited !')
            return redirect('home')
        else:
            messages.error(request, "There's Problem in inputs")
            return redirect('home')
    context = {
        'TitleForm' : TitleForm(instance = current_title),
    }
    return render(request, 'pages/edit-main-interface.html', context)

def manage_products(request):
    context = {
        'products' : Product.objects.all().order_by('-id'),
    }
    return render(request, 'pages/manage_products.html', context)

@csrf_exempt
def delete_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id = product_id)
        BASE_DIR = Path(__file__).resolve().parent.parent
        # For delete Product Images
        for product_image in product.images.all():
            path_image = product_image.image.path
            if os.path.exists(path_image):
                os.remove(path_image)
        # For delete Product
        product.delete()
        return JsonResponse({
            'status' : 'Deleted',
        })

def add_product(request):
    if request.method == 'POST':
        product = ProductForm(request.POST)
        if product.is_valid():
            new_product = product.save()
            product_images = request.FILES.getlist('images')
            for product_image in product_images:
                ProductImage.objects.create(
                    product = new_product,
                    image = product_image,
                )
            messages.success(request, 'product successfully added !')
            return redirect('home')


    context = {
        'ProductForm' : ProductForm(),
    }
    return render(request, 'pages/add-product.html', context)

def update_sizes(request):
    context = {
        'products' : Product.objects.all(),
    }
    return render(request, 'pages/update-sizes.html', context)

def update_product_sizes(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        update_size_form = UpdateSizesForm(request.POST, instance=product)
        if update_size_form.is_valid():
            update_size_form.save()
            messages.success(request, 'Product Sizes is Updated')
            return redirect('home')
        else:
            messages.error(request, "Product Sizes isn't Updated")
            return redirect('home')
    context = {
        'update_product_sizes' : UpdateSizesForm(instance=product),
        'product' : product,
    }
    return render(request, 'pages/update-product-sizes.html', context)

def view_orders(request):
    context = {
        'orders' : Order.objects.all(),
    }
    return render(request, 'pages/view_orders.html', context)

def order(request, id):
    context = {
        'order' : Order.objects.get(id = id),
        'order_items' : Order.objects.get(id = id).order_items.all(),
    }
    return render(request, 'pages/order.html', context)

def delete_order(request, id):
    if(request.user.is_authenticated):
        order_deleted = Order.objects.get(id = id)
        order_deleted.delete()
        return redirect('view-orders')