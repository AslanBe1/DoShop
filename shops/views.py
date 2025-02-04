from django.shortcuts import render, get_object_or_404

from shops.models import Product


# Create your views here.

def index(request):
    products = Product.objects.all()

    context = {
        'products':products
    }
    return render(request, 'shops/product-list.html', context=context)

def detail(request, pk):
    product = get_object_or_404(Product, id=pk)

    context = {
        'product':product
    }
    return render(request,'shops/product-details.html',context=context)


def customer(request):
    return render(request,  'shops/customers.html')

def customer_details(request):
    return render(request,'shops/customer-details.html')