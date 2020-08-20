from shop.models import Product, Category, Comment, OrderItem, Order
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from shop.forms import AddProductForm, EditProductForm
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView, View
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


class OrderSummaryView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'order': order
            }
            return render(self.request, 'shop/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("shop:shop")



def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.products.filter(product__pk=product.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("shop:order_summary")
        else:
            order.products.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("shop:order_summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.products.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("shop:order_summary")

def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.products.filter(product__pk=product.pk).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            order.products.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("shop:order_summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("shop:detail_product", pk=pk)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("shop:shop")

def remove_single_item_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.products.filter(product__pk=product.pk).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.products.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("shop:order_summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("shop:shop")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("shop:shop")

def empty_cart(request):
	Order.objects.filter(user=request.user, ordered=False).delete()
	messages.info(request, "your cart is emptied")
	return redirect("shop:order_summary")