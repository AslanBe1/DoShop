from django.urls import path
from shops import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product-deteil', views.detail, name='detail'),
    path('customer', views.customer, name='customer'),
    path('customers-detail', views.customer_details, name='customer_details'),
]