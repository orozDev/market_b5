from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.list_products),
    path('products/<int:id>/', views.detail_products),
]