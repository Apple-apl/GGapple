from django.shortcuts import render

def main_func(request):
    return render(request, template_name='main.html')

def products_func(request):
    return render(request, template_name='products.html')

def main_page(request):
    return render(request, 'main.html')

def products_page(request):
    return render(request, 'products.html')

def cart(request):
    cart_items = request.session.get('cart', [])
    return render(request, 'cart.html', {'cart_items': cart_items})

def add_to_cart(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        
        if product_name:
            cart = request.session.get('cart', [])
            
            cart.append(product_name)
            
            request.session['cart'] = cart
            
            return redirect('cart')
    
    return redirect('products')