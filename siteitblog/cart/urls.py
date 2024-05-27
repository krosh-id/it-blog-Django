from django.urls import path
from . import views
from .views import CardListAddDeleteView, ListProductView, ProductView

app_name = 'cart'

urlpatterns = [
    path('', CardListAddDeleteView.as_view(), name='cart_sum'),
    path('add/<int:product_id>/', CardListAddDeleteView.as_view(), name='cart_add'),
    path('remove/<int:product_id>/', CardListAddDeleteView.as_view(), name='cart_remove'),
    path('list/', ListProductView.as_view(), name='product_list_all'),
    path('list/<slug:cat_slug>', ListProductView.as_view(), name='product_list'),
    path('product/<int:product_id>', ProductView.as_view(), name='product'),
]
