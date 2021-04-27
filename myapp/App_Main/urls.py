from django.urls import path
from . import views
app_name='App_Main'
urlpatterns = [
path('', views.order,name='main'),
path('parcel/', views.create_parcel,name='parcel'),
path('deliver_parcel/<pk>/', views.deliver_parcel,name='deliver_parcel'),
path('my_orders/', views.merchant_orders,name='my_orders'),
]
