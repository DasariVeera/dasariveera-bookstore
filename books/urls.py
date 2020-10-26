from django.urls import   path
from .views import *

urlpatterns = [
     path('about/', about, name="about"),
     path('', books, name="book-list"),
     path('books/checkout', checkout, name="checkout"),
     path('books/search_results', search, name="search_results"),
     path('books/orders', completed_orders, name="completed_orders"),
     path('books/<int:pk>/', read, name="read"),
     path('books/<pk>', detail, name="book-detail"),
     path('books/<str:operation>/<pk>', add_to_cart, name="add_to_cart"),
     path('books/add_to_cart_ajax/', add_to_cart_ajax, name="add_to_cart_ajax"),
     path('user', profile, name="profile"),

     # wrong url handling
     # path('<path:execption>/', error_404_view, name="error"),
     ]