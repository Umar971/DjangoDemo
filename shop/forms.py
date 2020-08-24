from django import forms
from .models import Product, Category
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    shipping_zip = forms.CharField(required=False)



choices = Category.objects.all().values_list('name', 'name')

choice_list = []

for cat in choices:
    choice_list.append(cat)


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title','price', 'description', 'stock' ,'owner', 'category' ,'discount_price', 'product_image', 'serial_number')

        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title of your Product here'}),
            'price' : forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_price' : forms.NumberInput(attrs={'class': 'form-control'}),
            'owner' : forms.TextInput(attrs={'class': 'form-control','value':'', 'id':'user_id', 'type':'hidden'}),
            # 'owner' : forms.Select(attrs={'class': 'form-control'}),
            'category' : forms.Select(choices= choice_list, attrs={'class': 'form-control'}),
            'stock' : forms.NumberInput(attrs={'class': 'form-control'}),
            'description' : forms.Textarea(attrs={'class': 'form-control'}),
            'serial_number' : forms.TextInput(attrs={'class': 'form-control','value':'', 'id':'serial_num', 'type':'hidden'}),
            
        }

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title','price', 'description', 'stock' ,'owner', 'category' ,'discount_price', 'product_image', 'serial_number')

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


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        }))




class PaymentForm(forms.Form):
    stripeToken = forms.CharField(required=False)
