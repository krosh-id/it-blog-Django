import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import View, ListView, DetailView
from django.shortcuts import get_object_or_404, render

from cart.cart import Cart
from cart.models import Product
from siteitblog import settings


# добавить декоратор который добавляет профиль пользователя
class CardListAddDeleteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        profile = self.request.user
        return render(request, 'cart/cart.html', {'cart': cart, 'profile': profile})

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


class ListProductView(LoginRequiredMixin, ListView):
    template_name = "cart/product_list.html"
    context_object_name = 'products'
    allow_empty = False

    def get_queryset(self):
        if self.kwargs.get('cat_slug'):
            # добавить проверку товаров из корзины
            return Product.objects.filter(category__slug=self.kwargs['cat_slug']).all()
        else:
            return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context['products'][0].category
        context['cat_selected'] = category.name
        context['profile'] = self.request.user
        context['cart'] = self.request.session.get(settings.CART_SESSION_ID)
        print(context['cart'])
        return context


class ProductView(LoginRequiredMixin, DetailView):
    pass
