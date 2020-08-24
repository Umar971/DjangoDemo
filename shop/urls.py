from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
	path('index/', views.index, name='index'),
	path('create_product/', views.ProductCreateView.as_view(), name='create_product'),
	path('detail_product/<int:pk>', views.ProductDetailView.as_view(), name='detail_product'),
	path('delete_product/<int:pk>', views.ProductDeleteView.as_view(), name='product_delete'),
	path('update_product/<int:pk>', views.ProductUpdateView.as_view(), name='product_update'),
	path('shop/', views.ProductListView.as_view(), name='shop'),
	path('create_comment/<int:pk>', views.CommentCreateView, name='create_comment'),
	path('update_comment/<int:pk>', views.CommentUpdateView.as_view(), name='update_comment'),
	path('delete_comment/<int:pk>', views.CommentDeleteView.as_view(), name='delete_comment'),
	path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
	path('remove_from_cart/<int:pk>', views.remove_from_cart, name='remove_from_cart'),
	path('empty_cart/', views.empty_cart, name='empty_cart'),
	path('remove_product_from_cart/<int:pk>', views.remove_single_item_from_cart, name='remove_product_from_cart'),
	path('order_summary/', views.OrderSummaryView.as_view(), name='order_summary'),
	path('order_summary_session/', views.OrderSummaryViewSession, name='order_summary_session'),
	path('view_cart', views.view_cart, name= 'view_cart'),
	path('checkout/', views.CheckoutView.as_view(), name='checkout'),
	path('payment/', views.PaymentView.as_view(), name='payment'),
]