
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, TagsOnOrdersView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('tags/by-order/<int:pk>/', TagsOnOrdersView.as_view(), name='order-tag-list'),
    path('', OrderListCreateView.as_view(), name='order-list'),

]