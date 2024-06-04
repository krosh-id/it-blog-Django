from django.urls import path

from orders.views import OrderFormView, OrdersView, OrderEditView

app_name = 'orders'

urlpatterns = [
    path('', OrdersView.as_view(), name='orders'),
    path('remove/', OrderEditView.as_view(), name='orders'),
    path('form/', OrderFormView.as_view(), name='form'),
    path('<int:order_id>/', OrderFormView.as_view(), name='chat'),
]