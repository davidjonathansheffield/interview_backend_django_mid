
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, OrderListBetweenView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('', OrderListCreateView.as_view(), name='order-list'),
    path('between/<str:start_date>/<str:embargo_date>/', OrderListBetweenView.as_view(), name='order-list-between'),
]