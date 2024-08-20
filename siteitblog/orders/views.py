import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from cart.cart import Cart
from orders.forms import OrderForm, EditInformationOrderForm
from orders.models import Order


class OrderFormView(LoginRequiredMixin, View):
    '''
        Оформление заказа по форме и очистка корзина
    '''
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    data = {}

    def get(self, request):
        cart = Cart(request)
        form = self.form_class()
        self.data['profile'] = request.user
        self.data['cart'] = cart
        self.data['form'] = form
        return render(request, self.template_name, self.data)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cart = Cart(request) # исправить получение
            product_list = [item['product'] for item in cart]
            data = form.cleaned_data
            order = Order(
                full_name=data['first_name'] + ' ' + data['last_name'],
                email=data['email'],
                mobile_number=data['mobile_number'],
                address=data['address'],
                total_price=cart.total_products_price,
                user=self.request.user,
            )
            order.save()
            order.products.set(product_list)
            order.save()
            return redirect('order:orders')
        return render(request, self.template_name, self.data)


class OrderEditView(LoginRequiredMixin, View):
    def delete(self, request):
        """
            Удаление\отмена заказа
        """
        body_request = json.loads(request.body.decode("utf-8"))
        order = get_object_or_404(Order, id=body_request.get('orderId'))
        if order.status == 'PROCESSING':
            order.delete()
            return JsonResponse({'status': 'remove'})
        else:
            return HttpResponse(status=403)

    def patch(self, request):
        '''
            Обновление данных о заказе
        '''
        body_request = json.loads(request.body.decode("utf-8"))
        order = get_object_or_404(Order, id=body_request.get('orderId'))
        return JsonResponse({'status': 'updated'})


class OrdersView(LoginRequiredMixin, ListView):
    template_name = "orders/orders.html"
    context_object_name = 'orders'

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('orders.change_order'):
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        cart = Cart(self.request)
        cart.clear()

        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        return context


class OrderInfo(LoginRequiredMixin, UpdateView):
    model = Order
    fields = ['total_price', 'status', 'date_complete']
    template_name = 'orders/order_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = context.get('order').products.all()
        context['profile'] = self.request.user
        return context
