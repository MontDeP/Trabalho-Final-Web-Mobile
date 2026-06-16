from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Avaliacao
from .forms import AvaliacaoForm
from .serializers import SerializadorAvaliacao


class ListarAvaliacoes(LoginRequiredMixin, ListView):
    model = Avaliacao
    template_name = 'avaliacao/listar.html'
    context_object_name = 'itens'


class CadastrarAvaliacao(LoginRequiredMixin, CreateView):
    model = Avaliacao
    form_class = AvaliacaoForm
    template_name = 'avaliacao/novo.html'
    success_url = reverse_lazy('listar_avaliacoes')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class EditarAvaliacao(LoginRequiredMixin, UpdateView):
    model = Avaliacao
    form_class = AvaliacaoForm
    template_name = 'avaliacao/editar.html'
    success_url = reverse_lazy('listar_avaliacoes')


class DeletarAvaliacao(LoginRequiredMixin, DeleteView):
    model = Avaliacao
    template_name = 'avaliacao/deletar.html'
    success_url = reverse_lazy('listar_avaliacoes')


class APIListarAvaliacoes(ListCreateAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = SerializadorAvaliacao

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class APIAvaliacaoDetalhe(RetrieveUpdateDestroyAPIView):
    queryset = Avaliacao.objects.all()
    serializer_class = SerializadorAvaliacao
    permission_classes = [IsAuthenticated]
