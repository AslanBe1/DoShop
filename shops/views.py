from audioop import reverse
from typing import Optional
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
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

    paginator = Paginator(products, 1)
    page_number = request.GET.get('page','1')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
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
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')

        if not rating:
            rating = 1

        Comment.objects.create(product=product, name=name, email=email, comment=comment, rating=int(rating))
        return redirect('shops:detail', pk=pk)

    return redirect('shops/product-details.html', pk=product.id)


@login_required
def create_product(request):
    form =  ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shops:index')
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
            return redirect('shops:detail', pk)

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
        return redirect('shops:index')
    except Product.DoesNotExist as e:
        print(e)


@login_required
def create_attribute(request):
        form =  AttributeModelForm()
        if request.method == 'POST':
            form = AttributeModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('shops:create_attribute')

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
            form = AttributeValueModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('shops:create_attribute_value')

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
                return redirect('shops:product-attribute')

        else:
            form = ProductAttributeForm()

        context = {
            'form': form,
        }

        return render(request, 'shops/product-attribute.html', context)