from django.shortcuts import render, redirect
from django.utils import timezone


PRODUCTS_CATALOG = {
    "Комплектующие": {
        "Процессор Ryzen 5 7600": 22000,
        "Процессор Ryzen 7 7700X": 35000,
        "Процессор Ryzen 9 7900X": 52000,
        "Процессор Intel Core i5-14600K": 32000,
        "Процессор Intel Core i7-14700K": 48000,
        "Видеокарта RTX 4060": 31000,
        "Видеокарта RTX 4060 Ti": 42000,
        "Видеокарта RTX 4070 Ti": 55000,
        "Видеокарта RTX 4080 Super": 95000,
        "Материнская плата B650": 15000,
        "Материнская плата B760": 13000,
        "Оперативная память DDR5 32GB": 18000,
        "Оперативная память DDR5 64GB": 32000,
        "Блок питания 750W": 8500,
        "Блок питания 1000W": 14000,
        "Корпус ATX Mid-Tower": 6500,
        "Кулер башенный 120мм": 4500,
        "СЖО 240мм": 9500,
    },
    "Ноутбуки": {
        "Ноутбук Air 14": 65000,
        "Ультрабук S5 Lite": 55000,
        "Ноутбук X1 Pro": 95000,
        "Gaming M1 Ultra": 130000,
        "Gaming M3 Titan": 185000,
        "Ноутбук Office 15": 45000,
    },
    "Мониторы": {
        'Монитор 24" FHD 144Hz': 18000,
        'Монитор 27" QHD 165Hz': 32500,
        'Монитор 27" 4K IPS': 39000,
        'Монитор 32" 4K IPS': 48000,
        'Монитор 34" UltraWide': 72000,
        'Монитор 49" Super UltraWide': 115000,
    },
    "Хранение данных": {
        "SSD 500GB NVMe": 6500,
        "SSD 1TB NVMe": 12000,
        "SSD 2TB NVMe": 19000,
        "SSD 4TB NVMe": 34000,
        "HDD 4TB": 9000,
        "HDD 8TB": 16000,
        "Внешний SSD 1TB": 11000,
        "Картридер USB-C": 2500,
    },
    "Периферия": {
        "Механическая клавиатура RGB": 8500,
        "Клавиатура TKL Pro": 11000,
        "Мышь игровая 16K DPI": 4500,
        "Мышь офисная беспроводная": 1800,
        "Наушники с микрофоном": 9500,
        "Наушники беспроводные ANC": 14500,
        "Веб-камера Full HD": 5500,
        "Веб-камера 4K": 12000,
        "Микрофон студийный USB": 7500,
        "Коврик XXL": 1500,
    },
    "Аксессуары": {
        "Кабель HDMI 2.1": 1200,
        "Кабель DisplayPort": 1000,
        "Хаб USB-C 7-в-1": 3200,
        "Кресло игровое": 28000,
        "Подставка для ноутбука": 2500,
        "Чистящий набор": 800,
    },
}

PRICE_INDEX = {
    name: price
    for items in PRODUCTS_CATALOG.values()
    for name, price in items.items()
}

def products(request):
    return render(request, 'products.html', {'products_catalog': PRODUCTS_CATALOG})

def main_func(request):
    return render(request, template_name='main.html')

def main_page(request):
    return render(request, 'main.html')

def products_page(request):
    # ГЛАВНОЕ ИСПРАВЛЕНИЕ: передаём каталог в шаблон
    return render(request, 'products.html', {'products_catalog': PRODUCTS_CATALOG})


def normalize_cart(raw):
    """Приводит корзину к новому формату (словарь), если в сессии лежит старый список"""
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, list):
        # старый формат: список названий — преобразуем, цены возьмём из справочника
        new_cart = {}
        for name in raw:
            if name in PRICE_INDEX:
                new_cart[name] = {"price": PRICE_INDEX[name], "qty": 1}
        return new_cart
    return {}

def cart(request):
    cart_data = normalize_cart(request.session.get('cart', {}))
    total = sum(item["price"] * item["qty"] for item in cart_data.values())
    return render(request, 'cart.html', {'cart_data': cart_data, 'total': total})

def add_to_cart(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        if product_name and product_name in PRICE_INDEX:
            cart = normalize_cart(request.session.get('cart', {}))
            if product_name not in cart:
                cart[product_name] = {"price": PRICE_INDEX[product_name], "qty": 0}
            cart[product_name]["qty"] += 1
            request.session['cart'] = cart
            request.session.modified = True
        return redirect('products')
    return redirect('products')

def remove_from_cart(request, product_name):
    cart = request.session.get('cart', {})
    if product_name in cart:
        del cart[product_name]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('cart')

def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    return redirect('cart')

def contacts(request):
    message_sent = False

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        topic = request.POST.get('topic')
        text = request.POST.get('text')

        if name and email and topic and text:
            message_sent = True
            # Пока просто отмечаем успех; позже сюда можно добавить
            # сохранение в базу или отправку письма

    return render(request, 'contacts.html', {'message_sent': message_sent})

def checkout(request):
    if request.method == 'POST':
        cart_data = request.session.get('cart', {})
        if cart_data:
            total = sum(item["price"] * item["qty"] for item in cart_data.values())

            orders = request.session.get('orders', [])
            order_number = 'TS-' + timezone.localtime().strftime('%Y%m%d%H%M%S')
            order = {
                'number': order_number,
                'date': timezone.localtime().strftime('%d.%m.%Y %H:%M'),
                'items': [
                    {'name': name, 'price': item['price'], 'qty': item['qty']}
                    for name, item in cart_data.items()
                ],
                'total': total,
            }
            orders.append(order)
            request.session['orders'] = orders
            request.session.modified = True

            # Очищаем корзину
            request.session['cart'] = {}
            request.session.modified = True

            return redirect('orders')
    return redirect('cart')

def orders(request):
    # Берём только заказы с номером — старые битые записи отбрасываем
    orders_list = [
        o for o in reversed(request.session.get('orders', []))
        if o.get('number')
    ]
    return render(request, 'orders.html', {'orders': orders_list})


def cancel_order(request, order_number):
    if request.method == 'POST':
        orders = request.session.get('orders', [])
        request.session['orders'] = [
            o for o in orders if o.get('number') != order_number
        ]
        request.session.modified = True
    return redirect('orders')
