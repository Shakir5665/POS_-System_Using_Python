from django.shortcuts import render,redirect
from .models import Product,OrderItem,Order

# function to display product list
def product_list(request):
    products = Product.objects.all()
    return render(request,'products.html',{'products':products})


# function to get cart items
def get_cart(request):
    return request.session.setdefault('cart',{})

# function to add to cart
def add_to_cart(request , product_id):
    cart = get_cart(request)

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1
    
    request.session.modified = True

    return redirect('cart_view')


# function to display the cart items
def cart_view(request):
    
    cart = get_cart(request)
    items = []
    total = 0

    for product_id , quantity in cart.items():
        product = Product.objects.get(id = product_id)
        subTotal = product.price * quantity
        total += subTotal

        items.append(
            {
                'product':product,
                'quantity': quantity,
                'subTotal':subTotal
            }
        )

    return render(request, 'cart.html', {'items':items , 'total':total})

# function to remove item from cart
def remove_from_cart(request,product_id):

    cart = get_cart(request)
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id] # remiving item

        request.session.modified = True
    
    return redirect('cart_view')

def clear_cart(request):

    cart = get_cart(request)

    cart.clear() # make empty the cart dictionary

    request.session.modified = True
    
    return redirect('cart_view')


def checkout(request):

    cart = request.session.get('cart',{})

    if not cart:
        redirect('product_list')
    
    total = 0
    order = Order.objects.create(total_amount=0)

    for product_id,quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal =product.price * quantity
        total += subtotal

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            subTotal=subtotal
        )

        # Reduce stock
        product.stock -= quantity
        product.save()

        

    order.total_amount = total
    order.save()

    # Clear cart
    request.session['cart'] = {}
        


    return render(request, 'checkout_success.html', {'order': order})



