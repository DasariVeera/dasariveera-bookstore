from django.shortcuts import render, redirect, get_object_or_404 , reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.db.models import Q
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
        orders, created = Order.objects.get_or_create(user=request.user,order_completion_status=False)
    except:
        orders, created = Order.objects.get_or_create(user=request.user,order_completion_status=False)
    context = {'books':books, 'order':orders, 'books_bought':books_bought}
    
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
def checkout(request):
    books = Book.objects.all()
    order, created = Order.objects.get_or_create(user=request.user,order_completion_status=False)
    orderItems = order.orderitem_set.all()
    context = {'orderItems':orderItems, 'order':order}
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
