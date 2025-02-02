from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'shops/product-list.html')

def detail(request):
    return render(request,'shops/product-details.html')

def customer(request):
    return render(request,'shops/customers.html')

def customer_details(request):
    return render(request,'shops/customer-details.html')