from django.conf.urls import url
from . import views


urlpatterns = [
    # отображение корзины
    url(r'^$', views.cart_detail, name='cart_detail'),
    # обновление количества товара
    url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
    # удаление товара
    url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
]
