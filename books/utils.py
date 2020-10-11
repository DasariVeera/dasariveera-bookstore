from django.shortcuts import render, redirect, get_object_or_404 , reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import *

from .models import Book

def read(request, pk):
    book1 = Book.objects.get(id=pk)
    books_bought = []
    orders = Order.objects.filter(user=request.user)
    for order in orders:
        if order.order_completion_status:
            orderitems = order.orderitem_set.all()
            bought = [item.book.id for item in orderitems]
            books_bought +=bought
    if pk in books_bought:
        context = {'book':book1}
        return render(request, 'read.html', context)
    else:
        context = {'id':pk}
        return render(request, 'no_permisson.html', context)