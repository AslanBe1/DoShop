from audioop import reverse
from typing import Optional
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from shops.forms import CommentModelForm, ProductModelForm, AttributeModelForm, AttributeValueModelForm, \
    ProductAttributeForm
from shops.models import Product, ProductImages, Category, ProductAttribute, Comment, Attribute, AttributeValue


# Create your views here.

def app1_view(request):
    url = reverse('customers:customer.html')
    return HttpResponseRedirect(url)

def index(request, category_id:Optional[int]=None):
    categories = Category.objects.all()
    products = Product.objects.all()
    product_attributes = ProductAttribute.objects.filter()
    search_query = request.GET.get('q','')

    if search_query:
        products = Product.objects.filter(name__icontains=search_query)

    if category_id:
        products = Product.objects.filter(category_id = category_id)
    context = {
        'products':products,
        'categories':categories,
    }
    return render(request,  'shops/product-list.html', context=context)

def detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    comments = Comment.objects.filter(product=product,is_negative=False)

    context = {
        'product':product,
        'comments':comments,
    }
    return render(request,'shops/product-details.html',context=context)


def comment(request, pk):
    product = get_object_or_404(Product, id=pk)
    form = CommentModelForm()
    if request.method == 'POST':
        form = CommentModelForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('detail', pk)

    context = {
        'product':product,
        'form':form,
    }
    return render(request, 'shops/product-details.html', context=context)


@login_required
def create_product(request):
    form =  ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductModelForm()

    context = {
        'form': form
    }
    return render(request, 'shops/create-product.html', context)

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    form = ProductModelForm(instance=product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('detail', pk)

    context = {
        'form':form,
        'product':product,
    }
    return render(request, 'shops/edit-product.html', context=context)


@login_required
def delete_product(request, pk):
    try:
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return redirect('index')
    except Product.DoesNotExist as e:
        print(e)


@login_required
def create_attribute(request):
        form =  AttributeModelForm()
        if request.method == 'POST':
            form = AttributeModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('create_attribute')

        else:
            form = AttributeModelForm()

        context = {
            'form': form
        }

        return render(request, 'shops/add_atribute.html', context)

@login_required
def create_attribute_value(request):
        form =  AttributeValueModelForm()
        if request.method == 'POST':
            form = AttributeModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('create_attribute_value')

        else:
            form = AttributeValueModelForm()

        context = {
            'form': form
        }
        return render(request, 'shops/add_attribute_value.html', context)

@login_required
def product_attribute_value(request):
        form =  ProductAttributeForm()
        if request.method == 'POST':
            form = ProductAttributeForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('product-attribute')

        else:
            form = ProductAttributeForm()

        context = {
            'form': form,
        }

        return render(request, 'shops/add_attribute_value.html', context)