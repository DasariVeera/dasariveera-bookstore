from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404 , reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
import json
from django.core import serializers
from .models import *

from .models import Book
# Create your views here.



@login_required
def profile(request):
    order = Order.objects.get(user=request.user, order_completion_status=False)
    context = {'order':order}
    return render(request, 'profile.html', context)


def about(request):
    try:
        order = Order.objects.get(user=request.user, order_completion_status=False)
        context = {'order':order}
    except:
        context = {}

    return render(request, 'about.html', context)

@login_required
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
    

@login_required
def books(request):
    books = Book.objects.all()
    books_bought = []
    try:
        orders = Order.objects.filter(user=request.user)
        for order in orders:
            if order.order_completion_status:
                orderitems = order.orderitem_set.all()
                bought = [item.book.id for item in orderitems]
                books_bought += bought
        orders_ongo, created = Order.objects.get_or_create(user=request.user,order_completion_status=False)
    except:
        orders_ongo, created = Order.objects.get_or_create(user=request.user,order_completion_status=False)
    context = {'books':books, 'order':orders_ongo, 'books_bought':books_bought}
    
    return render(request, 'books/book_list.html', context)
# class BooksListView(ListView):
#     model = Book
#     context_object_name = "books"
    
#     def  get_context_data(self, **kwargs):
#         user = get_user_model()
#         order, created = Order.objects.get_or_create(user=user.username,order_completion_status=False)
#         context = super(BooksListView, self).get_context_data(**kwargs)
#         context.update({'get_total_cart_items':order.get_total_cart_items})
#         return context

@login_required
def detail(request, pk):
    book = Book.objects.get(id=pk)
    books_bought = []
    try:
        orders = Order.objects.filter(user=request.user, order_completion_status=True)
        for order in orders:
            orderitems = order.orderitem_set.all()
            # book_detail  = 
            bought = [item.book.id for item in orderitems]
            books_bought += bought
        orders, created = Order.objects.get_or_create(user=request.user,order_completion_status=False)
    except:
        orders, created = Order.objects.get_or_create(user=request.user,order_completion_status=False)
    context = {'book':book, 'order':orders, 'books_bought':books_bought}
    
    return render(request, 'books/book_detail.html', context)


# class BooksDetailView(DetailView):
#     model = Book
#     context_object_name = "book"

@login_required
def add_to_cart(request, operation, pk):
    user = request.user
    book = get_object_or_404(Book, id=pk)
    order, created = Order.objects.get_or_create(user=user,order_completion_status=False)
    orderItem, created = OrderItem.objects.get_or_create(book=book, order=order)

    # orderItem.quantity +=1
    # orderItem.save()
    if operation=="add" or operation=="addition":
        orderItem.quantity +=1
    elif operation =="remove":
        orderItem.quantity -=1
    elif operation =="delete":
        orderItem.quantity = 0

    orderItem.save()
    if orderItem.quantity <=0:
        orderItem.delete()
    if operation=="addition":
        return redirect('book-list')
    else:
        return redirect('checkout')

@login_required
def add_to_cart_ajax(request):
    data = json.loads(request.body)
    pk= data['itemid']
    operation = data['operation']
    user = request.user
    book = get_object_or_404(Book, id=pk)
    order, created = Order.objects.get_or_create(user=user,order_completion_status=False)
    orderItem, created = OrderItem.objects.get_or_create(book=book, order=order)

    # orderItem.quantity +=1
    # orderItem.save()
    if operation=="add" or operation=="addition":
        orderItem.quantity +=1
    elif operation =="remove":
        orderItem.quantity -=1
    elif operation =="delete":
        orderItem.quantity = 0

    orderItem.save()
    if orderItem.quantity <=0:
        orderItem.delete()
    cartvalue = {'cartItem':orderItem.quantity, 'total_cart_items':order.get_total_cart_items}
    print(cartvalue)

    return JsonResponse(cartvalue,safe=False)

def books_not_bought(user):
    books = Book.objects.all()
    all_books_ids = [book for book in books]
    books_not_bought = []
    books_bought = []
    try:
        orders = Order.objects.filter(user=user, order_completion_status=True)
        for order in orders:
            orderitems = order.orderitem_set.all()
            bought = [item.book.id for item in orderitems]
            books_bought += bought
        for book in all_books_ids:
            if book.id in books_bought:
                continue
            else:
                books_not_bought.append(book)
        return books_not_bought
    except:
        pass
    return True

@login_required
def checkout(request):
    user=request.user
    books_not_bought_list = books_not_bought(user)

    paginator= Paginator(books_not_bought_list, 3)
        
    books = Book.objects.all()
    order, created = Order.objects.get_or_create(user=request.user,order_completion_status=False)
    orderItems = order.orderitem_set.all()
    # paginator= Paginator(books_not_bought_list, 3)
    # print('books', paginator.count)
    page  = paginator.page(1)
    context = {'orderItems':orderItems, 'order':order, 'books':books , 'page':page}
    details = {}
    if request.method == "POST":
        for page in paginator.page_range:
            book  = paginator.page(page)
            book_data = book.object_list[0]
            details[page]={'id':book_data.id, 'image':book_data.image.url}
            if page == 1:
                details['prev']=False
            else:
                details['prev']=True
            if page == paginator.num_pages:
                details['next']=False
            else:
                details['next']=True
        page_data = json.loads(request.body)
        # pages = serializers.serialize('json', [page,])
        page_info = {'page':details}
        print('bookssssssssssssssssssss', page_data)
        return JsonResponse(page_info,safe=False)
    return render(request, 'checkout.html', context)

@login_required
def payment(request):
    books = Book.objects.all()
    order, created = Order.objects.get_or_create(user=request.user,order_completion_status=False)
    orderItems = order.orderitem_set.all()
    context = {'orderItems':orderItems, 'order':order}
    if request.method == "POST":
        # order, created = Order.objects.get_or_create(user=request.user,order_completion_status=False)
        order.order_completion_status = True
        order.date_of_order=datetime.now()
        order.save()
        # alert("Payment Success!!")
        return redirect('book-list')
    return render(request, 'payment.html', context)

@login_required
def completed_orders(request):
    orderItems = []
    ongoing_order, craeted = Order.objects.get_or_create(user=request.user, order_completion_status=False)
    orders = Order.objects.filter(user=request.user, order_completion_status=True)
    for order in orders:
        orderItemset = order.orderitem_set.all()
        for Items in orderItemset:
            orderItems.append(Items)
    # orderItems = [order.orderitem_set.all() for order in orders]
    context = {'orderItems':orderItems, 'order':ongoing_order}
    return render(request, 'completed_orders.html', context)

# class SearchResultsView(ListView):
#     model = Book
#     template_name = "search_results.html"
#     context_object_name = 'search_book_results'

#     def get_queryset(self):
#         query = self.request.GET['val1']
#         return Book.objects.filter(title__icontains=query )

@login_required
def search(request):
    query = request.GET['search_value']
    books = Book.objects.filter(Q(title__icontains = query) | Q(author__icontains = query) )
    books_bought = []
    try:
        orders = Order.objects.filter(user=request.user)
        for order in orders:
            if order.order_completion_status:
                orderitems = order.orderitem_set.all()
                bought = [item.book.id for item in orderitems]
                books_bought += bought
        orders, created = Order.objects.get_or_create(user=request.user,order_completion_status=False)
    except:
        orders, created = Order.objects.get_or_create(user=request.user,order_completion_status=False)
    context = {'books':books, 'order':orders, 'books_bought':books_bought}
    
    return render(request, 'search_results.html', context)

# def error_handler(request):
#     return redirect('book-list')



def error_404_view(request, execption):
    return render(request, 'error_404.html')
def error_handler(request, execption, template_name="error_404.html"):
    response.status_code=404
    return response