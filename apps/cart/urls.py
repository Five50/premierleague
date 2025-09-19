from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('summary/', views.get_cart_summary, name='cart_summary'),
    path('checkout/', views.checkout, name='checkout'),
    path('api/data/', views.cart_api_data, name='cart_api_data'),
]