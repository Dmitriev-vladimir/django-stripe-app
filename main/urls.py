from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('item/<int:item_id>/', views.item),
    path('buy/<int:item_id>/', views.buy),
    path('order/', views.order, name='cart'),
    path('order/buy/', views.order_buy),
    path('success/', views.success)
]
