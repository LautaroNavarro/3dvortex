# import mercadopago
from infra.views import BaseView
from infra.request.errors import ForbiddenError
from prints.models.order import Order
from django.http import HttpResponse
from django.conf import settings


class OrderIpnView(BaseView):

    required_body = False

    def validate(self, request, order_id, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        print('request META: {}'.format(request.META))
        print('request GET: {}'.format(request.GET))
        if not request.META['MERCADO_PAGO_TOKEN'] == settings.MERCADO_PAGO_TOKEN:
            raise ForbiddenError('Invalid request')

    def run(self, request, order_id, *args, **kwargs):
        topic = request.GET.get('topic', 'payment')
        if topic == 'payment':
            return HttpResponse(status=200)
        # mp = mercadopago.MP(settings.MERCADO_PAGO_TOKEN)
        # mp_order = mp.get('/merchant_orders/{}'.format(request.GET['id']))
        # TODO: Check if the price is the correct one
        Order.objects.filter(id=order_id).update(
            payment_status=Order.PaymentStatus.PAID,
            status=Order.Status.READY_TO_BE_PRINTED,
        )
        return HttpResponse(status=200)
