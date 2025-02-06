from django.urls import path, include
from customers import views

urlpatterns = [
    path('customer', views.customers, name='customer'),
    path('customers-detail/<int:pk>/', views.customer_details, name='customer_details'),
    path('edit-customer/<int:pk>/', views.edit_customer, name='edit_customer'),
    path('create-customer/', views.create_customer, name='create_customer'),
    path('delete-customer/<int:pk>/', views.delete_customer, name='delete_customer'),
]