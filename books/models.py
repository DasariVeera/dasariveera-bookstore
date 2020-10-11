from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    author = models.CharField(max_length=150)
    eBook = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, max_length=500)
    pdf = models.FileField(upload_to='pdf', default="default.pdf", max_length=500)
    description = models.TextField(default="This books does not contain any description. Please refer to author and title of the Book")

    def __str__(self):
        return  self.title

class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_of_order = models.DateTimeField(auto_now_add=True)
    order_completion_status = models.BooleanField(default=False)

    @property
    def get_total_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total
    
    @property
    def get_total_cart_price(self):
        order_items = self.orderitem_set.all()
        total = sum([(item.quantity * item.book.price) for item in order_items])
        return total

    def __str__(self):
        return str(self.id)

class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.book.title

class Address(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=500, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    pincode = models.CharField(max_length=6, null=True)

    def __str__(self):
        return self.address