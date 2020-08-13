from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name='accounts-home'),
    path("products/",views.products,name='products'),
    path("customers/<str:pk>/",views.customer,name='customer'),

]
