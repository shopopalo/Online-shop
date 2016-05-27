from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def order_created(order_id):
    """отправка письма с оповещением об успешно созданном заказе"""
    order = Order.objects.get(id=order_id)
    subject = _('Заказ #%(order_id)s') % {'order_id': order.id}
    message = _('Dear %(f_name)s, you have successfully placed an order. Your order id is %(order_id)s') % {
        'f_name': order.first_name, 'order_id': order.id}

    mail_sent = send_mail(subject, message, 'phonxis@gmail.com', [order.email])

    return mail_sent