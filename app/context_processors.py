from .models import Product

def cart_length(request):
    cart = request.session.get('cart', {})
    pop_keys = []
    for key in cart.keys():
        product_id, product_size = key.split('_')
        if (not Product.objects.filter(id = product_id).exists()):
            pop_keys.append(key)
        else:
            product = Product.objects.get(id = product_id)
            out_of_stuck_founded = False
            size_founded = False
            for size in product.sizes.all():
                if size.size == 'OUT OF STOCK':
                    out_of_stuck_founded = True
                    pop_keys.append(key)
                    break
            if not out_of_stuck_founded:
                for size in product.sizes.all():
                    if size.size == product_size:
                        size_founded = True
                        break
                if not size_founded:
                    pop_keys.append(key)
    for key in pop_keys:
        cart.pop(key)
    request.session['cart'] = cart
    return {
        'cart_length' : len(cart),
    }