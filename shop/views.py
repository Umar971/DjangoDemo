import stripe
from django.conf import settings
from shop.models import Product, Category, Comment, OrderItem, Order, Address, Payment, Coupon
from carts.models import Carts, CartsItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from shop.forms import AddProductForm, EditProductForm, CouponForm, PaymentForm
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView, View
from django.urls import reverse_lazy, reverse
from .forms import CheckoutForm

stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

def index(request):
    count_items_in_cart = CartsItem.objects.all().count()
    return render(request, 'shop/index.html', {'count_items':count_items_in_cart})


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

    def get_context_data(self,*args, **kwargs):
        count_items = CartsItem.objects.all().count()
        context = super(ProductListView,self).get_context_data(*args,**kwargs)
        context['count_items']= count_items
        return context

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
            if order.coupon:
                discount = order.get_total_without_coupon() - order.get_total()
            else:
                discount = 0
            context = {
                'order': order,
                'discount': round(discount, 2)
            }
            return render(self.request, 'shop/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("shop:shop")

def OrderSummaryViewSession(LoginRequiredMixin, request):
        try:
            cart = get_user_cart(request)
            object_cart = Carts.objects.get(id=cart.id)
            
            context = {
                'object': object_cart,
            }
            return render(request, 'carts/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(request, "You do not have an active order")
            return redirect("shop:shop")


# def get_user_cart(request):
#     """Retrieves the shopping cart for the current user."""
#     cart_id = None
#     cart = None
#     # If the user is logged in, then grab the user's cart info.
#     cart_id = request.session.get('cart_id')
#     print(cart_id)
#     if not cart_id:
#         cart = Carts()
#         cart.save()
#         request.session['cart_id'] = cart.id
#         print("new cart")
#     else:
#         cart = Carts.objects.get(id=cart_id)
#         print("old cart")
#     return cart
# @login_required
# def view_cart(request):
#     cart = get_user_cart(request)
#     cart_items = CartsItem.objects.filter(carts=cart)
#     order_total = 0
#     for item in cart_items:
#         order_total += (item.product.price * item.quantity)
#     return render(request, 'carts/view_cart.html',{'cart_items':cart_items})

# def get_cart_count(request):
#     cart = get_user_cart(request)
#     total_count = 0
#     cart_items = CartsItem.objects.filter(carts=cart)
#     for item in cart_items:
#         total_count += item.quantity
#     return total_count

def update_cart_info(request):
    request.session['cart_count'] = get_cart_count(request)
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated and not request.user.is_anonymous:
        order_item, created = OrderItem.objects.get_or_create(product=product,user=request.user,ordered=False)
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
            order = Order.objects.create(user=request.user, ordered_date=ordered_date)
            order.products.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("shop:order_summary")
    # else:
    #     cart = get_user_cart(request)
    #     object_cart = Carts.objects.get(id=cart.id)
    #     if CartsItem.objects.filter(product__pk=product.pk).exists():
    #         cart_item, created = CartsItem.objects.get_or_create(product=product)
    #         cart_item.quantity += 1
    #         cart_item.save()
    #         messages.info(request, "This item quantity was updated.")
    #         return render(request, 'carts/order_summary.html', {'object':object_cart})
    #     else:
    #         cart_item, created = CartsItem.objects.get_or_create(product=product)
    #         cart.products.add(cart_item)
    #         messages.info(request, "This item was added to your cart.")
    #         return render(request, 'carts/order_summary.html', {'object':object_cart})

@login_required
def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated and not request.user.is_anonymous:
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
    # else:
    #     cart = get_user_cart(request)
    #     object_cart = Carts.objects.get(id=cart.id)
    #     if CartsItem.objects.filter(product__pk=product.pk).exists():
    #         cart_item = CartsItem.objects.get(product=product)
    #         cart.products.remove(cart_item)
    #         cart_item.delete()
    #         cart.save()
    #         messages.info(request, "This item was removed successfully.")
    #         return render(request, 'carts/order_summary.html', {'object':object_cart})
    #     else:
    #         messages.info(request, "This item was not in your cart.")
    #         return redirect("shop:detail_product", pk=pk)


@login_required
def remove_single_item_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated and not request.user.is_anonymous:
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
    # else:
    #     cart = get_user_cart(request)
    #     object_cart = Carts.objects.get(id=cart.id)
    #     if CartsItem.objects.filter(product__pk=product.pk).exists():
    #         cart_item = CartsItem.objects.get(product=product)
    #         if cart_item.quantity > 1:
    #             cart_item.quantity -= 1
    #             cart_item.save()
    #         else:
    #             cart.products.remove(cart_item)

    #             cart_item.delete()
    #         cart.save()
    #         messages.info(request, "This item quantity was updated.")
    #         return render(request, 'carts/order_summary.html', {'object':object_cart})
    #     else:
    #         messages.info(request, "This item was not in your cart.")
    #         return redirect("shop:detail_product", pk=pk)

# @login_required
# def empty_cart(request):
# 	Order.objects.filter(user=request.user, ordered=False).delete()
# 	messages.info(request, "your cart is emptied")
# 	return redirect("shop:order_summary")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            if order.coupon:
                discount = order.get_total_without_coupon() - order.get_total()
            else:
                discount = 0
            context = {
                'form': form,
                'order': order,
                'discount': round(discount, 2),
            }
            messages.info(self.request, "You are on placement of order page")
            return render(self.request, "shop/checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("shop:shop")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                shipping_address = form.cleaned_data.get("shipping_address")
                shipping_address2 = form.cleaned_data.get("shipping_address2")
                shipping_country = form.cleaned_data.get("shipping_country")
                shipping_zip = form.cleaned_data.get("shipping_zip")

                address = Address(
                    user = self.request.user,
                    street_address = shipping_address, 
                    apartment_address = shipping_address2,
                    country = shipping_country, 
                    zip = shipping_zip
                    )
                address.save()
                order.shipping_address = address
                order.save()
                return redirect("shop:payment")
            else:
                return redirect("shop:checkout")
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("shop:order_summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.shipping_address:
            return render(self.request, "shop/payment.html", {'order':order})
        else:
            messages.warning(
                self.request, "You have not added a shipping address")
            return redirect("shop:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        # token = stripe.Token.create(card={ "number": "4242424242424242", "exp_month": 8, "exp_year": 2021, "cvc": "314",})
        amount = int(order.get_total() * 100)
        try:
            charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="usd",
                        source="tok_visa",
                    )
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            order.ordered = True
            order.payment = payment
            order.save()
            messages.success(self.request, "Your Order Was Successful")
            return redirect("shop:shop")

        except stripe.error.CardError as e:
          # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect("shop:shop")
        except stripe.error.RateLimitError as e:
          # Too many requests made to the API too quickly
          messages.warning(self.request, "RateLimitError")
          return redirect("shop:shop")
        except stripe.error.InvalidRequestError as e:
          # Invalid parameters were supplied to Stripe's API
          messages.warning(self.request, "InvalidRequestError")
          return redirect("shop:shop")
        except stripe.error.AuthenticationError as e:
          # Authentication with Stripe's API failed
          # (maybe you changed API keys recently)
          messages.warning(self.request, "AuthenticationError")
          return redirect("shop:shop")
        except stripe.error.APIConnectionError as e:
          # Network communication with Stripe failed
          messages.warning(self.request, "APIConnectionError")
          return redirect("shop:shop")
        except stripe.error.StripeError as e:
          # Display a very generic error to the user, and maybe send
          # yourself an email
          messages.warning(self.request, "StripeError")
          return redirect("shop:shop")
        except Exception as e:
          # Something else happened, completely unrelated to Stripe
          messages.warning(self.request, "Something Went Wrong Please Try Again")
          return redirect("shop:shop")


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.filter(code=code, expiry_date__gte = timezone.now())
        return coupon
    except ObjectDoesNotExist:
        messages.warning(request, "This coupon does not exist")
        return redirect("shop:checkout")


class ApplyCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                coupon = get_coupon(self.request, code)
                if coupon:
                    order.coupon = coupon[0]
                    order.save()
                    messages.success(self.request, "Successfully added coupon")
                    return redirect("shop:order_summary")
                else:
                    messages.warning(self.request, "This coupon does not exist")
                    return redirect("shop:order_summary")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("shop:order_summary")
        else:
            messages.warning(self.request, "Invalid Promo code")
            return redirect("shop:order_summary")


