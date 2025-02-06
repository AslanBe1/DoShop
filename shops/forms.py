from django import forms
from shops.models import Comment, Product, Attribute, AttributeValue, ProductAttribute


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name','email','content']


class AttributeModelForm(forms.ModelForm):
    class Meta:
        model = Attribute
        fields = '__all__'

class AttributeValueModelForm(forms.ModelForm):
    class Meta:
        model = AttributeValue
        fields = '__all__'

class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = '__all__'