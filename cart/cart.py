from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon


class Cart(object):

    def __init__(self, request):
        """ инициализируем корзину """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        # если в данной сессии нет корзины
        # создаем пустую
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart
        # запоминаем код купона
        self.coupon_id = self.session.get('coupon_id')

    def __len__(self):
        """ Считаем общее количество товаров в корзине """
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """ 
        Связываем товары из корзины
        с товарами из базы данных по id
        """
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавляем товар в корзину или обновляем количество
        уже имеющегося товара в корзине
        """
        product_id = str(product.id)

        # добавляем товар в корзину
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """ удаляем товар из корзины """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        # обновить корзину
        self.session[settings.CART_SESSION_ID] = self.cart
        # указать что сессия была изменена
        self.session.modified = True

    def clear(self):
        """ удаление корзины """
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_total_price(self):
        # определие суммы всех товаров
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_discount(self):
        # определение суммы скидки
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        # возвращение суммы заказа учитывая скидку
        return self.get_total_price() - self.get_discount()
