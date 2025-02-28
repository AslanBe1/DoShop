import csv
import json
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from customers.forms import CustomerModelForm
from customers.models import Customer

# Create your views here.

def customers(request):
    search_query = request.GET.get('q', '')
    customers = Customer.objects.all()

    if search_query:
        customers = customers.filter(name__icontains=search_query)

    context = {
        'customers': customers
               }
    return render(request, 'customers/customer.html', context)

def customer_details(request,pk):
    customer = Customer.objects.get(pk=pk)

    context = {
        'customer': customer
    }

    return render(request,'customers/customer-details.html', context)


def create_customer(request):
    form =  CustomerModelForm()
    if request.method == 'POST':
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customers:customer')
    else:
        form = CustomerModelForm()

    context = {
        'form': form
    }
    return render(request, 'customers/create_customers.html', context)


def edit_customer(request,pk):
    customer = Customer.objects.get(pk=pk)
    form = CustomerModelForm(instance=customer)
    if request.method == 'POST':
        form = CustomerModelForm(request.POST, request.FILES ,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers:customer_details', pk)

    context = {
        'form': form,
        'customer': customer
    }
    return render(request,'customers/edit_custopmers.html', context=context)



def delete_customer(request, pk):
    try:

        customer = get_object_or_404(Customer, id=pk)
        customer.delete()
        return redirect('customers:customer')

    except Customer.DoesNotExist as e:
        print(e)


def load_details(request):
    format = request.GET.get('format','')
    response = None

    if format == 'json':
        response = HttpResponse(content_type='application/json')
        data = list(Customer.objects.all().values('name','email','address','phone','VAT_number','description','password'))
        for customer in data:
            customer['phone'] = str(customer['phone'])
        response.write(json.dumps(data, indent=4))
        response['Content-Disposition'] = 'attachment; filename="customers.json"'


    elif format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="customers.csv"'
        writer = csv.writer(response)
        writer.writerow(['Id','Name','email','phone','address','description','VAT_number','password'])
        for customer in Customer.objects.all():
            writer.writerow([customer.id,customer.name,customer.email,customer.phone,customer.address,customer.VAT_number,customer.password])

    elif format == 'xlsx':
        customs = Customer.objects.all().values()
        df = pd.DataFrame(list(customs))
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="customers.xlsx"'
        writer = pd.ExcelWriter(response)
        
    else:
        response = HttpResponse(status=404)
        response.content = 'BAD REQUEST'

    return response






# Aggregate
# from customers.models import Customer
# from django.db.models import Max, Min, Count, Avg
# Customer.objects.all().aggregate(Count('id'))
# Result: {'id__count': 3}


# Customer.objects.all().aggregate(Avg('id'))
# Result: {'id__avg': 6.0}

# Customer.objects.all().aggregate(result = Avg('id'))
# {'result': 6.0}


# Annotate
# from customers.models import Customer
# from django.db.models import Max, Min, Count, Avg

# Customer.objects.all().annotate(name_count=Count('name'))
# Result: <QuerySet [<Customer: Hasan => +998653652547>, <Customer: Oppoq qor => +998775556633>, <Customer: Oppoq => +998991464146>]>


# custom = Customer.objects.all().annotate(name_count=Count('name'))
# >>> for i in custom:
# ...     print(i.email,i.name_count)
# Result: vcsjgvguS@gmail.com 1, qoraqr@gmail.com 1, qoraqor@gmail.com 1

# custom = Customer.objects.all().annotate(name_count=Count('name')).order_by('-name_count')
# Result: <QuerySet [<Customer: Hasan => +998653652547>, <Customer: Oppoq qor => +998775556633>, <Customer: Oppoq => +998991464146>]>



# product = Product.objects.all().annotate(product_count=Count('name')).order_by('-price')
# Result: <QuerySet [<Product: Oppoq qor>, <Product: MacBook Pro>]>



# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------Har Bir categoryda nechta product bor--------------------------------------
# category = Category.objects.all().annotate(category_count=Count('products'))

# for i in category:
# ...     print(i.name, i.category_count)
# Result: Laptops 1, zdbz 1

# ------------------- Har bir categoryda eng qimmat productlar  --------------------------
# category = Category.objects.all().annotate(category_count=Max('products__price'))

# for i in category:
# print(i.name,i.category_count)
# Result: Laptops 777777.77, zdbz 8888888.88


# ------------------------------ Har bir categoryda eng arzon product ------------------------------
# category = Category.objects.all().annotate(category_count=Min('products__price'))

# for i in category:
# print(i.name,i.category_count)
# Result: Laptops 7777.00
# zdbz 8888888.88 Bu categoryda yagona product


# ------------------------------ Har bir categoryda ortacha product ------------------------
# category = Category.objects.all().annotate(category_count=Avg('products__price'))

# for i in category:
# print(i.name,i.category_count)
# Result: Laptops 392777.385000000000, zdbz 8888888.880000000000