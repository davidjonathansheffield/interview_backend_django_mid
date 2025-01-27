from django.shortcuts import render
from rest_framework import generics
from rest_framework.exceptions import ValidationError

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class TagsOnOrdersView(generics.ListAPIView):
    serializer_class = OrderTagSerializer

    def get_queryset(self):
        """ Returns all tags on an order."""
        try:
            return Order.objects.get(pk=self.kwargs.get('pk')).tags.all()
        except Order.DoesNotExist:
            raise ValidationError('Order does not exist')
