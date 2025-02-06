from django.urls import path
from shops import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product-detail/<int:pk>/', views.detail, name='detail'),
    path('category-choice/<int:category_id>/', views.index, name='category'),
    path('product-comment/<int:pk>/', views.comment, name='comment'),
    path('create-product/', views.create_product, name='create_product'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('customer/<int:pk>/', views.app1_view, name='customer'),
    path('create-attrbute', views.create_attribute, name='create_attribute'),
    path('create-attrbute-value', views.create_attribute_value, name='create_attribute_value'),
    path('product-attribute/', views.product_attribute_value, name='product-attribute'),
]