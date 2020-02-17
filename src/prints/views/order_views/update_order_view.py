
import json
from infra.views import BaseView
from helpers.view_helpers import require_admin
from infra.request.errors import (
    NotFoundError,
    BadRequestError,
)
from prints.models.order import Order
from django.http import JsonResponse


class UpdateOrderView(BaseView):

    content_type = 'application/json'

    schema = {
        'type': 'object',
        'properties': {
            'status': {'type': 'integer'},
        },
        'required': ['status'],
        'additionalProperties': False,
    }

    required_body = True

    @require_admin
    def validate(self, request, order_id, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        body = json.loads(request.body)
        order = Order.objects.filter(id=order_id)
        if not order:
            raise NotFoundError('The provided order id does not exists')
        self.validate_status_is_known(body['status'])
        self.validate_status_change(
            body['status'],
            order[0].status,
            self.user_payload['access_level'],
        )

    @staticmethod
    def validate_status_change(new_status, actual_status, user_access_level):
        #  TODO validate change is valid inside order life cycle
        pass

    @staticmethod
    def validate_status_is_known(new_status):
        if new_status not in [
            Order.Status.NOT_READY_TO_BE_PRINTED,
            Order.Status.READY_TO_BE_PRINTED,
            Order.Status.PRITING,
            Order.Status.READY_TO_BE_DELIVERED,
            Order.Status.DELIVERED,
        ]:
            raise BadRequestError('The provided status does not exists.')

    def run(self, request, order_id, *args, **kwargs):
        body = json.loads(request.body)
        order = Order.objects.get(id=order_id)
        order.status = body['status']
        order.save()
        return JsonResponse(order.serialized)
