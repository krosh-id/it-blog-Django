import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.views import View
from django.views.generic import ListView

from cart.cart import Cart
from orders.forms import OrderForm
from orders.models import Order



class OrderFormView(LoginRequiredMixin, View):
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
            cart_list = [item for item in cart]
            data = form.cleaned_data
            order = Order(
                full_name=data['first_name'] + data['last_name'],
                email=data['email'],
                mobile_number=data['mobile_number'],
                address=data['address'],
                total_price=cart.total_products_price,
                user=self.request.user
            )
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
        return Order.objects.filter(user=self.request.user).all()

    def get_context_data(self, **kwargs):
        cart = Cart(self.request)
        cart.clear()

        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user
        return context
