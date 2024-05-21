from django.urls import path
from . import views
from .views import CardListAddDeleteView

app_name = 'cart'

urlpatterns = [
    path('', CardListAddDeleteView.as_view(), name='cart_sum'),
    path('add/<int:product_id>/', CardListAddDeleteView.as_view(), name='cart_add'),
    path('remove/<int:product_id>/', CardListAddDeleteView.as_view(), name='cart_remove'),
]
