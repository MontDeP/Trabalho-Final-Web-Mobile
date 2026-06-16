from django.urls import path
from . import views

urlpatterns = [
    path('listar/', views.listar, name='listar_veiculo'),
    path('novo/', views.novo, name='novo_veiculo'),
    path('editar/<int:id>/', views.editar, name='editar_veiculo'),
    path('deletar/<int:id>/', views.deletar, name='deletar_veiculo'),
    path('api/', views.VeiculoAPIView.as_view(), name='api_veiculo'),
    path('api/<int:pk>/', views.VeiculoDetailAPIView.as_view(), name='api_veiculo_detail'),
]
