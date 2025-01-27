from django.shortcuts import render
from rest_framework import generics

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class OrderListByTagView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        tag_name = self.kwargs['tag']
        return Order.objects.filter(tags__name=tag_name)
