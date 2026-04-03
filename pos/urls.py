from django.urls import path
from . import views

urlpatterns = [
    path('',views.product_list,name='product_list'),
    path('add/<int:product_id>/' , views.add_to_cart , name='add_to_cart'),
    path('cart/' , views.cart_view , name='cart_view'),
    path('remove/<int:product_id>/' , views.remove_from_cart , name="remove_from_cart"),
    path('clear/' , views.clear_cart , name='clear_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
]