from decimal import Decimal
from django.conf import settings

from cart.models import Product


# Корзина товаров для сессии
class Cart:
    cart = None
    total_products_price = None

    def __init__(self, request):
        """
        Инициализировать корзину.
        """
        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID)
        if not self.cart:
            # сохранить пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
            self.cart = cart

    def __iter__(self):
        """
        Прокрутить товарные позиции корзины в цикле и
        получить товары из базы данных.
        """
        self.total_products_price = 0
        product_ids = self.cart.keys()
        # получить объекты product и добавить их в корзину
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            self.total_products_price += item['total_price']
            yield item

    def __len__(self):
        """
        Подсчитать все товарные позиции в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1):
        """
        Добавить товар в корзину либо обновить его количество.
        """
        product_id = product.id
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        self.cart[product_id]['quantity'] = quantity
        self.save()

    def remove(self, product):
        """
        Удалить товар из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        # пометить сеанс как "измененный",
        # чтобы обеспечить его сохранен
        self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.cart.values())

    def clear(self):
        # удалить корзину из сеанса
        del self.session[settings.CART_SESSION_ID]
        self.save()
