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

]