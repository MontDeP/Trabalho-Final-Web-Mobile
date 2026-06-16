from django.urls import path
from . import views

urlpatterns = [
    path('listar/', views.listar, name='listar_anuncio'),
    path('novo/', views.novo, name='novo_anuncio'),
    path('editar/<int:id>/', views.editar, name='editar_anuncio'),
    path('deletar/<int:id>/', views.deletar, name='deletar_anuncio'),
    path('api/', views.AnuncioAPIView.as_view(), name='api_anuncio'),
    path('api/<int:pk>/', views.AnuncioDetailAPIView.as_view(), name='api_anuncio_detail'),
]
