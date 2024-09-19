from django.urls import path, include
from . import views

urlpatterns = [
    path('products/', views.ListCreateProductApiView.as_view()),
    path('products/create-attributes/', views.create_product_attributes),
    path('products/attributes/<int:id>/', views.update_delete_product_attributes),
    path('products/<int:id>/', views.DetailUpdateDeleteProductApiView.as_view()),
    path('auth/', include('api.auth.urls')),
]