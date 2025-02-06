from webbrowser import get

from django.contrib.auth.decorators import login_required
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
            return redirect('customer')
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
            return redirect('customer_details', pk)

    context = {
        'form': form,
        'customer': customer
    }
    return render(request,'customers/edit_custopmers.html', context=context)



def delete_customer(request, pk):
    try:

        customer = get_object_or_404(Customer, id=pk)
        customer.delete()
        return redirect('customer')

    except Customer.DoesNotExist as e:
        print(e)