from django.urls import path
from shops import views
app_name = 'shops'

urlpatterns = [
    path('', views.index, name='index'),
    path('product-detail/<slug:slug>/', views.detail, name='detail'),
    path('category-choice/<slug:slug>/', views.index, name='category'),
    path('product-comment/<int:pk>/', views.comment, name='comment'),
    path('create-product/', views.CreateProduct.as_view(), name='create_product'),
    path('edit-product/<int:pk>/', views.EditProduct.as_view(), name='edit_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('customer/<int:pk>/', views.app1_view, name='customer'),
    path('create-attrbute', views.CreateAttribute.as_view(), name='create_attribute'),
    path('create-attrbute-value', views.AttributeValeu.as_view(), name='create_attribute_value'),
    path('product-attribute/', views.CreateProductAttribute.as_view(), name='product-attribute'),
]