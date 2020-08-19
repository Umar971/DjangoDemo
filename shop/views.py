from shop.models import Product
from django.shortcuts import render
from django.http import HttpResponse
from shop.forms import AddProductForm, EditProductForm
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy

def index(request):
	return render(request, 'shop/index.html', {})


class ProductCreateView(CreateView):
	model = Product
	form_class = AddProductForm
	template_name = 'shop/create_product.html'
	success_url = reverse_lazy('shop:shop')


class ProductDetailView(DetailView):
	model = Product
	template_name = 'shop/detail_product.html'


class ProductListView(ListView):
	model = Product
	template_name = 'shop/shop.html'


class ProductDeleteView(DeleteView):
	model = Product
	template_name = 'shop/product_delete.html'
	success_url = reverse_lazy('shop:shop')


class ProductUpdateView(UpdateView):
	model = Product
	form_class = EditProductForm
	template_name = 'shop/update_product.html'
	# fields = "__all__"
	success_url = reverse_lazy('shop:shop')