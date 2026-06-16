from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.APIListarAvaliacoes.as_view(), name='api_avaliacoes'),
    path('api/<int:pk>/', views.APIAvaliacaoDetalhe.as_view(), name='api_avaliacao_detalhe'),
    path('', views.ListarAvaliacoes.as_view(), name='listar_avaliacoes'),
    path('novo/', views.CadastrarAvaliacao.as_view(), name='nova_avaliacao'),
    path('editar/<int:pk>/', views.EditarAvaliacao.as_view(), name='editar_avaliacao'),
    path('deletar/<int:pk>/', views.DeletarAvaliacao.as_view(), name='deletar_avaliacao'),
]
