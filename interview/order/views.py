from django.shortcuts import render
from rest_framework import generics

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer
from interview.utils import get_date_from_str
from rest_framework.exceptions import ValidationError


# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class OrderListBetweenView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        start_date = get_date_from_str(self.kwargs['start_date'])
        embargo_date = get_date_from_str(self.kwargs['embargo_date'])
        if not start_date or not embargo_date:
            raise ValidationError('Invalid date format, please use YYYY-MM-DD')

        return Order.objects.filter(start_date__gte=start_date, embargo_date__lte=embargo_date)
