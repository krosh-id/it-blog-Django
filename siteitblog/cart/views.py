import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseNotFound
from django.views.generic import View, ListView, DetailView
from django.shortcuts import get_object_or_404, render

from cart.cart import Cart
from cart.models import Product
from siteitblog import settings


# добавить декоратор который добавляет профиль пользователя
class CardListAddDeleteView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        for item in cart:
            print(item['product'], item['price'], item['quantity'], item['total_price'])
        profile = self.request.user
        context_data = {
            'cart': cart,
            'profile': profile
        }
        return render(request, 'cart/cart.html', context_data)

    def post(self, request, *args, **kwargs):
        """
        Добавление и обновление количества товара в сессии или корзины.
        """
        cart = Cart(request)
        body_request = request.body.decode("utf-8")
        product = get_object_or_404(Product, id=json.loads(body_request).get('productId'))
        # quantity = json.loads(body_request).get('quantity')
        cart.add(product=product) # quantity=quantity

        return JsonResponse({'status': 'add'})

    def delete(self, request, *args, **kwargs):
        """
        Удаление товара из сессии или корзины
        """
        cart = Cart(request)
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
        cart = self.request.session.get(settings.CART_SESSION_ID)
        if cart:
            context['cart'] = [int(item) for item in self.request.session.get(settings.CART_SESSION_ID).keys()]
        print(context.get('cart'))
        return context


class ProductView(LoginRequiredMixin, DetailView):
    pass
