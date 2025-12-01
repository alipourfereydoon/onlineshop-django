from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Product
from .forms import LoginForm

def index(request):
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('shop:index')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('shop:index')
    return render(request, 'shop/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('shop:index')    

def _get_cart(request):
    return request.session.setdefault('cart', {})

@require_POST
def api_add_to_cart(request):
# expects JSON {product_id: int, quantity: int}
    import json
    data = json.loads(request.body.decode('utf-8') or '{}')
    pid = str(data.get('product_id'))
    qty = int(data.get('quantity', 1))
    product = get_object_or_404(Product, pk=pid)
    cart = _get_cart(request)
    if pid in cart:
        cart[pid]['quantity'] += qty
    else:
        cart[pid] = {'name': product.name, 'price': str(product.price), 'quantity': qty}
    request.session.modified = True
    return JsonResponse({'ok': True, 'cart': cart})   

@require_POST
def api_remove_from_cart(request):
    import json
    data = json.loads(request.body.decode('utf-8') or '{}')
    pid = str(data.get('product_id'))
    cart = _get_cart(request)
    if pid in cart:
        del cart[pid]
        request.session.modified = True
    return JsonResponse({'ok': True, 'cart': cart}) 

def cart_view(request):
    cart = _get_cart(request)
    # prepare items list
    items = []
    total = 0
    for pid, info in cart.items():
        qty = int(info['quantity'])
        price = float(info['price'])
        subtotal = qty * price
        items.append({'product_id': pid, 'name': info['name'], 'price': price, 'quantity': qty, 'subtotal': subtotal})
        total += subtotal
    return render(request, 'shop/cart.html', {'items': items, 'total': total})    