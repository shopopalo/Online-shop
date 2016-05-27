from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
import weasyprint
from io import BytesIO
from orders.models import Order
from django.utils.translation import gettext_lazy as _


def payment_notification(sender, **kwargs):
    ipn_obj = sender
    print('payment')
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # заказ был успешно оплачен
        # invoice имеет вид ord12, где число соответствует
        # id заказа в системе
        order_id = ipn_obj.invoice.split('d')[1]
        print('order id -- ', order_id)
        order = get_object_or_404(Order, id=order_id)
        # изменить статус заказа на оплачен
        order.paid = True
        order.save()

        # для отправки pdf на email
        subject = _("Phonxis Shop. Invoice nr. %(order_id)s") % {'order_id': order.id}
        message = _('Please, find attached the invoice for your recent purchase.')
        email = EmailMessage(subject, message, 'phonxis@mail.com', [order.email])

        html = render_to_string('orders/order/pdf,html', {'order': order})
        out = BytesIO()
        stylesheets = [weasyprint.CSS(settings.STATIC_ROOT+'css/pdf.css')]
        weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
        email.attach('order_{}.pdf'.format(order.id), out.getvalue(), 'application/pdf')
        email.send()

valid_ipn_received.connect(payment_notification)
