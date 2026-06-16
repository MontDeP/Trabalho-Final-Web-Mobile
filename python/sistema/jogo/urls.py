from django.urls import path
from . import views

urlpatterns = [
    path('api/', views.APIListarJogos.as_view(), name='api_jogos'),
    path('api/<int:pk>/', views.APIJogoDetalhe.as_view(), name='api_jogo_detalhe'),
    path('', views.ListarJogos.as_view(), name='listar_jogos'),
    path('novo/', views.CadastrarJogo.as_view(), name='novo_jogo'),
    path('<int:pk>/', views.EditarJogo.as_view(), name='editar_jogo'),
    path('deletar/<int:pk>/', views.DeletarJogo.as_view(), name='deletar_jogo'),
]
