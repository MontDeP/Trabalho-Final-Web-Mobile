from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Jogo
from .forms import JogoForm
from .serializers import SerializadorJogo


class ListarJogos(LoginRequiredMixin, ListView):
    model = Jogo
    template_name = 'jogo/listar.html'
    context_object_name = 'itens'


class CadastrarJogo(LoginRequiredMixin, CreateView):
    model = Jogo
    form_class = JogoForm
    template_name = 'jogo/novo.html'
    success_url = reverse_lazy('listar_jogos')


class EditarJogo(LoginRequiredMixin, UpdateView):
    model = Jogo
    form_class = JogoForm
    template_name = 'jogo/editar.html'
    success_url = reverse_lazy('listar_jogos')


class DeletarJogo(LoginRequiredMixin, DeleteView):
    model = Jogo
    template_name = 'jogo/deletar.html'
    success_url = reverse_lazy('listar_jogos')


class APIListarJogos(ListCreateAPIView):
    queryset = Jogo.objects.all()
    serializer_class = SerializadorJogo

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]


class APIJogoDetalhe(RetrieveUpdateDestroyAPIView):
    queryset = Jogo.objects.all()
    serializer_class = SerializadorJogo
    permission_classes = [IsAuthenticated]
