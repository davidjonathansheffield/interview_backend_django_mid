import logging
from rest_framework import generics
from rest_framework.response import Response

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

from django.db import transaction

logger = logging.getLogger(__name__)

# Create your views here.

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class OrderDeactivateView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        It's highly likely that this method will attach additional functionality to the deactivation process.
        Perhaps an email to users indicating deactivation, for instance.

        For this reason it's important that this method avoid concurrency issues and transactional problems.

        """

        # Database lock starts here
        instance = Order.objects.select_for_update().get(pk=kwargs['pk'])

        instance.is_active = False
        instance.save()
        logger.info(f'Order {instance.id} deactivated.', extra={'order_id': instance.id})
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
