from django.urls import path, include
from . import views

urlpatterns = [
    path('products/', views.list_create_products),
    path('products/create-attributes/', views.create_product_attributes),
    path('products/attributes/<int:id>/', views.update_delete_product_attributes),
    path('products/<int:id>/', views.detail_update_product),
    path('auth/', include('api.auth.urls')),
]