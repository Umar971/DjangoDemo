from django import forms
from .models import Product, Category

choices = Category.objects.all().values_list('name', 'name')

choice_list = []

for cat in choices:
    choice_list.append(cat)


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title','price', 'description', 'stock' ,'owner', 'category' ,'discount_price', 'product_image')

        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title of your Product here'}),
            'price' : forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_price' : forms.NumberInput(attrs={'class': 'form-control'}),
            'owner' : forms.TextInput(attrs={'class': 'form-control','value':'', 'id':'user_id', 'type':'hidden'}),
            # 'owner' : forms.Select(attrs={'class': 'form-control'}),
            'category' : forms.Select(choices= choice_list, attrs={'class': 'form-control'}),
            'stock' : forms.NumberInput(attrs={'class': 'form-control'}),
            'description' : forms.Textarea(attrs={'class': 'form-control'}),
            
        }

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title','price', 'description', 'stock' ,'owner', 'category' ,'discount_price', 'product_image')

        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title of your Product here'}),
            'price' : forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_price' : forms.NumberInput(attrs={'class': 'form-control'}),
            # 'owner' : forms.TextInput(attrs={'class': 'form-control','value':'', 'id':'user_id', 'type':'hidden'}),
            # 'owner' : forms.Select(attrs={'class': 'form-control'}),
            'category' : forms.Select(choices= choice_list, attrs={'class': 'form-control'}),
            'stock' : forms.NumberInput(attrs={'class': 'form-control'}),
            'description' : forms.Textarea(attrs={'class': 'form-control'}),
            
        }



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

        widgets = {
         'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter blog catagory here'}),   
        }


