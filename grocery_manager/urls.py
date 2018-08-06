from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_scrape, name='product_scrape'),
]
