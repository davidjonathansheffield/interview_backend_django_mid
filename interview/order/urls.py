
from django.urls import path
from interview.order.views import OrderListByTagView, OrderListCreateView, OrderTagListCreateView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('', OrderListCreateView.as_view(), name='order-list'),
    path('by-tag/<str:tag>/', OrderListByTagView.as_view(), name='order-list-by-tag'),
]