from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .yasg import urlpatterns as url_doc
from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet)


urlpatterns = [
    path('products/', views.ListCreateProductApiView.as_view()),
    path('products/create-attributes/', views.CreateProductApiView.as_view()),
    path('products/attributes/<int:id>/', views.UpdateDeleteProduct.as_view()),
    path('products/<int:id>/', views.DetailUpdateDeleteProductApiView.as_view()),
    path('auth/', include('api.auth.urls')),
    path('', include(router.urls)),
]

urlpatterns += url_doc