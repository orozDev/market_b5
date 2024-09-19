from django.urls import path, include
from . import views

urlpatterns = [
    path('products/', views.ListCreateProductApiView.as_view()),
    path('products/create-attributes/', views.CreateProductApiView.as_view()),
    path('products/attributes/<int:id>/', views.UpdateDeleteProduct.as_view()),
    path('products/<int:id>/', views.DetailUpdateDeleteProductApiView.as_view()),
    path('auth/', include('api.auth.urls')),
]