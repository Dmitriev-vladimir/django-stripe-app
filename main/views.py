import json
import os

import stripe


from django.http import HttpResponse
from django.shortcuts import render, redirect
from dotenv import load_dotenv

from main.models import Item, Order

load_dotenv()


def index(request):
    items = Item.objects.all()
    return render(request, 'main/index.html', {'items': items})


def item(request, item_id):
    buy_item = Item.objects.filter(id=item_id)[0]
    stripe_key = os.environ['STRIPE_TEST_PUBLIC_KEY']
    return render(request, 'main/item.html', {'item': buy_item, 'key': stripe_key})


def buy(request, item_id):
    buy_item = Item.objects.filter(id=item_id)[0]
    stripe.api_key = os.environ['STRIPE_TEST_SECRET_KEY']
    stripe_price = int(buy_item.price * 100)
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': buy_item.name,
                },
                'unit_amount': stripe_price,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
    )
    response = HttpResponse()
    response.headers['session_id'] = session.id
    return response


def order(request):
    if request.method == 'POST':
        data = request.body.decode()
        current_url = request.headers.get('referer')
        item_id = json.loads(data)['id']
        operation = json.loads(data)['operation']
        if item_id == 0:
            Order.clean_order()
        else:
            temp = Order.objects.filter(item_id=item_id)
            if len(temp) == 0:
                current_item = Item.objects.filter(id=item_id)[0]
                Order.objects.create(item=current_item, quantity=1)
            elif operation == 'increase':
                temp[0].increase()
            else:
                temp[0].decrease()

        return redirect(current_url)

    order_list = Order.objects.all()
    total = Order.total_amount()
    empty = True if len(order_list) == 0 else False
    return render(request, 'main/cart.html', {
                'order_list': order_list,
                'empty': empty,
                'total': total,
                'key': os.environ['STRIPE_TEST_PUBLIC_KEY']
            }
    )


def order_buy(request):
    stripe.api_key = os.environ['STRIPE_TEST_SECRET_KEY']
    total = int(Order.total_amount() * 100)
    payment_intent_instance = stripe.PaymentIntent.create(
        amount=total,
        currency='rub',
        payment_method_types=['card']
    )
    response = HttpResponse()
    response.headers['data'] = payment_intent_instance.client_secret
    response.headers['key'] = os.environ['STRIPE_TEST_PUBLIC_KEY']

    return response


def success(request):
    Order.clean_order()
    return render(request, 'main/success.html')
