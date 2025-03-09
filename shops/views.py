from audioop import reverse
from itertools import product
from msvcrt import GetErrorMode

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from requests import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from shops.forms import CommentModelForm, ProductModelForm, AttributeModelForm, AttributeValueModelForm, ProductAttributeForm
from shops.models import Product, ProductImages, Category, ProductAttribute, Comment, Attribute, AttributeValue
from shops.serializers import ProductSerializer


# Create your views here.

def app1_view(request):
    url = reverse('customers:customer.html')
    return HttpResponseRedirect(url)

def index(request, slug=None):
    categories = Category.objects.all()
    products = Product.objects.all()
    product_attributes = ProductAttribute.objects.filter()
    search_query = request.GET.get('q','')

    if search_query:
        products = Product.objects.filter(name__icontains=search_query)

    if slug:
        products = Product.objects.filter(category__slug=slug)

    paginator = Paginator(products, 1)
    page_number = request.GET.get('page','1')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'products':products,
        'categories':categories,
    }

    return render(request,  'shops/product-list.html', context=context)


def detail(request, slug=None):
    product = get_object_or_404(Product, category__slug=slug)
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
            return redirect('shops:detail', pk)

    context = {
        'product':product,
        'form':form,
    }
    return render(request, 'shops/product-details.html', context=context)


# @login_required
# def create_product(request):
#     form =  ProductModelForm()
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('shops:index')
#     else:
#         form = ProductModelForm()
#
#     context = {
#         'form': form
#     }
#     return render(request, 'shops/create-product.html', context)

# @login_required
# def edit_product(request, pk):
#     product = get_object_or_404(Product, id=pk)
#     form = ProductModelForm(instance=product)
#     if request.method == 'POST':
#         form = ProductModelForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             return redirect('shops:detail', pk)
#
#     context = {
#         'form':form,
#         'product':product,
#     }
#     return render(request, 'shops/edit-product.html', context=context)


@login_required
def delete_product(request, pk):
    try:
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return redirect('shops:index')
    except Product.DoesNotExist as e:
        print(e)


# @login_required
# def create_attribute(request):
#         form =  AttributeModelForm()
#         if request.method == 'POST':
#             form = AttributeModelForm(request.POST, request.FILES)
#             if form.is_valid():
#                 form.save()
#                 return redirect('shops:create_attribute')
#
#         else:
#             form = AttributeModelForm()
#
#         context = {
#             'form': form
#         }
#
#         return render(request, 'shops/add_atribute.html', context)
#
# @login_required
# def create_attribute_value(request):
#         form =  AttributeValueModelForm()
#         if request.method == 'POST':
#             form = AttributeValueModelForm(request.POST, request.FILES)
#             if form.is_valid():
#                 form.save()
#                 return redirect('shops:create_attribute_value')
#
#         else:
#             form = AttributeValueModelForm()
#
#         context = {
#             'form': form
#         }
#         return render(request, 'shops/add_attribute_value.html', context)
#
#
# @login_required
# def product_attribute_value(request):
#         form =  ProductAttributeForm()
#         if request.method == 'POST':
#             form = ProductAttributeForm(request.POST, request.FILES)
#             if form.is_valid():
#                 form.save()
#                 return redirect('shops:product-attribute')
#
#         else:
#             form = ProductAttributeForm()
#
#         context = {
#             'form': form,
#         }
#
#         return render(request, 'shops/product-attribute.html', context)
#


class CreateProduct(CreateView):
    model = Product
    template_name = 'shops/create-product.html'
    form_class = ProductModelForm
    success_url = reverse_lazy("shops:index")

class EditProduct(UpdateView):
    model = Product
    template_name = 'shops/edit-product.html'
    form_class = ProductModelForm
    success_url = reverse_lazy("shops:index")

class CreateAttribute(CreateView):
    model = Attribute
    template_name = 'shops/add_atribute.html'
    form_class = AttributeModelForm
    success_url = reverse_lazy("shops:create_attribute")

class AttributeValeu(CreateView):
    model = Attribute
    template_name = 'shops/add_attribute_value.html'
    form_class = AttributeValueModelForm
    success_url = reverse_lazy("shops:create_attribute_value")

class CreateProductAttribute(CreateView):
    model = ProductAttribute
    template_name = 'shops/product-attribute.html'
    form_class = ProductAttributeForm
    success_url = reverse_lazy("shops:product-attribute")



class ProductLists(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        product = Product.objects.all()
        data = []
        for products in product:
            data.append({
                'id': products.id,
                'name': products.name,
                'description': products.description,
                'price': products.price,
                'discount': products.discount,
                'quantity': products.quantity,
                'rating': products.rating,
                'slug': products.slug,
            })
        return Response(data)


class ProductList(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        products = Product.objects.all()
        serializers = ProductSerializer(products, many=True)

        return Response(serializers.data, status=status.HTTP_200_OK)




class ProductDetail(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk, format=None):
        product = Product.objects.get(id=pk)
        serializers = ProductSerializer(product)

        return Response(serializers.data, status=status.HTTP_200_OK)