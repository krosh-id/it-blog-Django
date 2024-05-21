import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import View, ListView
from django.shortcuts import get_object_or_404, render

from cart.cart import Cart
from cart.models import Product


class CardListAddDeleteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        return render(request, 'cart/cart_sum.html', {'cart': cart})

    def post(self, request, *args, **kwargs):
        """
        Добавление и обновление количества товара в сессии или корзины.
        """
        cart = Cart(request)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            body_request = request.body.decode("utf-8")
            product = get_object_or_404(Product, id=json.loads(body_request).get('productId'))
            quantity = json.loads(body_request).get('quantity')
            cart.add(product=product,
                     quantity=quantity
                     )
            return JsonResponse({'status': 'add'})

    def delete(self, request, *args, **kwargs):
        """
        Удаление товара из сессии или корзины
        """
        cart = Cart(request)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            body_request = request.body.decode("utf-8")
            product = get_object_or_404(Product, id=json.loads(body_request).get('productId'))
            cart.remove(product)
            return JsonResponse({'status': 'remove'})

    def patch(self, request, *args, **kwargs):
        pass


# Create your views here.
class ListProductView(LoginRequiredMixin, ListView):
    template_name = "cart/cart.html"
    context_object_name = 'products'
    allow_empty = False

    def get_queryset(self):
        # добавить проверку товаров из корзины
        return Product.objects.filter(category__slug=self.kwargs['cat_slug']).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['products'][0].category
        context['cat_selected'] = category.name
        return context
