from shop.models import Product, Category, Comment
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from shop.forms import AddProductForm, EditProductForm
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse

def index(request):
	return render(request, 'shop/index.html', {})


class ProductCreateView(CreateView):
	model = Product
	form_class = AddProductForm
	template_name = 'shop/create_product.html'
	success_url = reverse_lazy('shop:shop')

	def get_context_data(self,*args, **kwargs):
		serial_num = Product.ran_gen_serial_num()
		context = super(ProductCreateView,self).get_context_data(*args,**kwargs)
		context['serial_num'] = serial_num
		return context


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

def CommentCreateView(request, pk):
	if request.method == 'POST':
		product = get_object_or_404(Product, pk=pk)
		body = request.POST['bodyofcomment']
		comment = Comment(product=product, name=request.user, body=body)
		comment.save()
		product.comment_set.add(comment)
		return HttpResponseRedirect(reverse('shop:detail_product', kwargs={'pk': pk}))

class CommentUpdateView(UpdateView):
	model = Comment
	template_name = 'shop/comment_update.html'
	fields = ['body',]

	def get_success_url(self):
          # if you are passing 'pk' from 'urls' to 'DeleteView' for company
          # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
          primary_key = self.kwargs['pk']
          comment = Comment.objects.get(pk = primary_key)
          product = Product.objects.get(pk=comment.product.pk)
          return reverse_lazy('shop:detail_product', kwargs={'pk': product.pk})


class CommentDeleteView(DeleteView):
	model = Comment
	template_name = 'shop/comment_delete.html'

	def get_success_url(self):
          # if you are passing 'pk' from 'urls' to 'DeleteView' for company
          # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
          primary_key = self.kwargs['pk']
          comment = Comment.objects.get(pk = primary_key)
          product = Product.objects.get(pk=comment.product.pk)
          return reverse_lazy('shop:detail_product', kwargs={'pk': product.pk})


