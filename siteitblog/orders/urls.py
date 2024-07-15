from django.urls import path

from orders.views import OrderFormView, OrdersView, OrderEditView, OrderInfo

app_name = 'orders'

urlpatterns = [
    path('', OrdersView.as_view(), name='orders'),
    path('edit/', OrdersView.as_view(), name='orders_edit'),
    path('remove/', OrderEditView.as_view(), name='order_remove'),
    path('form/', OrderFormView.as_view(), name='form'),
    path('<int:pk>/', OrderInfo.as_view(), name='chat'),
]