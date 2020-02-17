import pytz
import mercadopago
import json
from infra.views import BaseView
from helpers.view_helpers import require_jwt
from infra.request.errors import BadRequestError
from prints.models.material import Material
from prints.models.order import Order
from django.http import JsonResponse
from geopy.distance import geodesic
from printers.models.printer import Printer
from models.models.model import Model
from addresses.models.address import Address
from django.conf import settings
import datetime


class CreateOrderView(BaseView):

    content_type = 'application/json'

    schema = {
        'type': 'object',
        'properties': {
            'model': {'type': 'integer'},
            'scale': {'type': 'string'},
            'material': {'type': 'integer'},
            'address': {'type': 'integer'}
        },
        'required': ['model', 'scale', 'material', 'address'],
        'additionalProperties': False,
    }

    required_body = True

    @require_jwt
    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        body = json.loads(request.body)
        if not Model.objects.filter(id=body['model']).exists():
            raise BadRequestError('Invalid model id')
        if not Material.objects.filter(id=body['material']).exists():
            raise BadRequestError('Invalid material id')
        if not Address.objects.filter(id=body['address']).exists():
            raise BadRequestError('Invaid address id')
        if not Printer.objects.filter(material_id=body['material']).exists():
            raise BadRequestError('Currently we are not able to print this material.')

    @staticmethod
    def calculate_nearest_printer(material_id, address_lat, address_long):
        nearest_printer = None
        nearest_distance = 0
        for printer in Printer.objects.filter(material_id=material_id).select_related('address'):
            if nearest_printer is None:
                nearest_printer = printer
                nearest_distance = geodesic(
                    '{},{}'.format(address_lat, address_long),
                    '{},{}'.format(printer.address.latitude, printer.address.longitude)
                ).kilometers
            else:
                new_distance = geodesic(
                    '{},{}'.format(address_lat, address_long),
                    '{},{}'.format(printer.address.latitude, printer.address.longitude)
                ).kilometers
                if new_distance < nearest_distance:
                    nearest_printer = printer
                    nearest_distance = new_distance
        return nearest_printer

    @staticmethod
    def create_mp_preference(price, order_id, model_name, model_id, model_description, model_image_media_url):
        def get_formatted_datetime(datetime_to_convert):
            return '{}-{}-{}T{}:{}:{}.000+00:00'.format(
                datetime_to_convert.year,
                datetime_to_convert.month,
                datetime_to_convert.day,
                datetime_to_convert.hour,
                datetime_to_convert.minute,
                datetime_to_convert.second,
            )
        mp = mercadopago.MP(settings.MERCADO_PAGO_TOKEN)
        expiration_date_from = datetime.datetime.utcnow().replace(
            tzinfo=pytz.utc,
            microsecond=0
        )
        expiration_date_to = datetime.datetime.utcnow().replace(
            tzinfo=pytz.utc,
            microsecond=0
        ) + datetime.timedelta(0, 600)
        preference = {
            'items': [
                {
                    'id': model_id,
                    'description': 'Impresión 3d - {}'.format(model_description),
                    'picture_url': model_image_media_url,
                    'title': model_name,
                    'quantity': 1,
                    'currency_id': 'ARS',
                    'unit_price': float(price),
                }
            ],
            'back_urls': {
                # Once the payment finish mp redirect to these URLs
                'failure': '{}/payment_error/'.format(settings.BASE_URL),
                'success': '{}/orders/'.format(settings.BASE_URL),
            },
            'auto_return': 'approved',
            'notification_url': '{}/orders/{}/ipn'.format(settings.BASE_URL, order_id),
            'expires': True,
            "expiration_date_from": get_formatted_datetime(expiration_date_from),
            'expiration_date_to': get_formatted_datetime(expiration_date_to),
        }
        preferenceResult = mp.create_preference(preference)
        return preferenceResult['response']['id']

    def run(self, request, *args, **kwargs):
        body = json.loads(request.body)
        address = Address.objects.get(id=body['address'])
        printer = self.calculate_nearest_printer(body['material'], address.latitude, address.longitude)
        model = Model.objects.get(id=body['model'])
        material = Material.objects.get(id=body['material'])
        order = Order.objects.create(
            address=address,
            status=Order.Status.NOT_READY_TO_BE_PRINTED.value,
            payment_status=Order.PaymentStatus.NOT_PAID.value,
            price=model.calculate_price(material.price_per_kilogram, body['scale']),
            user_id=self.user_payload['id'],
            scale=body['scale'],
            printer=printer,
            material=material,
            model=model,
        )
        preference_id = self.create_mp_preference(
            order.price,
            order.id,
            model.name,
            model.id,
            model.description,
            model.image_media.url,
        )
        order.preference_id = preference_id
        order.save()
        return JsonResponse(order.serialized)
