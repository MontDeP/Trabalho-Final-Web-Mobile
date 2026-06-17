from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from sistema.permissions import IsOwnerOrReadOnly

from .models import Jogo
from .forms import JogoForm
from .serializers import SerializadorJogo


class ListarJogos(LoginRequiredMixin, ListView):
    model = Jogo
    template_name = 'jogo/listar.html'
    context_object_name = 'itens'

    def get_queryset(self):
        if self.request.GET.get('meus'):
            return Jogo.objects.filter(criado_por=self.request.user)
        return Jogo.objects.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['meus'] = bool(self.request.GET.get('meus'))
        return ctx


class CadastrarJogo(LoginRequiredMixin, CreateView):
    model = Jogo
    form_class = JogoForm
    template_name = 'jogo/novo.html'
    success_url = reverse_lazy('listar_jogos')

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


class EditarJogo(LoginRequiredMixin, UpdateView):
    model = Jogo
    form_class = JogoForm
    template_name = 'jogo/editar.html'
    success_url = reverse_lazy('listar_jogos')

    def get_queryset(self):
        if self.request.user.is_staff:
            return Jogo.objects.all()
        return Jogo.objects.filter(criado_por=self.request.user)


class DeletarJogo(LoginRequiredMixin, DeleteView):
    model = Jogo
    template_name = 'jogo/deletar.html'
    success_url = reverse_lazy('listar_jogos')

    def get_queryset(self):
        if self.request.user.is_staff:
            return Jogo.objects.all()
        return Jogo.objects.filter(criado_por=self.request.user)


class APIListarJogos(ListCreateAPIView):
    queryset = Jogo.objects.all()
    serializer_class = SerializadorJogo

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(criado_por=self.request.user)


class APIJogoDetalhe(RetrieveUpdateDestroyAPIView):
    queryset = Jogo.objects.all()
    serializer_class = SerializadorJogo
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
