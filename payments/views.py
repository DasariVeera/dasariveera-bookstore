import stripe
from django.shortcuts import render,redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from django.views.generic import TemplateView
from books.models import *
# Create your views here.

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
@login_required
def stripePayment(request):
    order, created = Order.objects.get_or_create(user=request.user,order_completion_status=False)
    orderItems = order.orderitem_set.all()
    context = {'stripe_key':settings.STRIPE_TEST_PUBLISHABLE_KEY, 'order':order, 'orderItems':orderItems}
    return render(request, 'payments/purchase.html', context)


@login_required
def charge(request):
    books = Book.objects.all()
    order, created = Order.objects.get_or_create(user=request.user,order_completion_status=False)
    orderItems = order.orderitem_set.all()
    context = {'orderItems':orderItems, 'order':order}
    if request.method == "POST":
        charge = stripe.Charge.create(
            amount = int(order.get_total_cart_price)*100,
            currency = "INR",
            description = "buy a book",
            source = request.POST['stripeToken']
        )
        # order, created = Order.objects.get_or_create(user=request.user,order_completion_status=False)
        order.order_completion_status = True
        order.save()
        # alert("Payment Success!!")
        return redirect('completed_orders')


# def charge(request):
#     if request.method == "POST":
#         charge = stripe.Charge.create(
#             amount = "1000",
#             currency = "INR",
#             description = "buy a book",
#             source = request.POST['stripeToken']
#         )
#     return render(request, 'payments/charge.html')

