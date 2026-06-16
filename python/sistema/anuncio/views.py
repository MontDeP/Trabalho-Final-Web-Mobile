from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Anuncio
from .forms import AnuncioForm
from .serializers import AnuncioSerializer


@login_required
def listar(request):
    anuncios = Anuncio.objects.all()
    return render(request, 'anuncio/listar.html', {'anuncios': anuncios})


@login_required
def novo(request):
    form = AnuncioForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listar_anuncio')
    return render(request, 'anuncio/novo.html', {'form': form})


@login_required
def editar(request, id):
    anuncio = get_object_or_404(Anuncio, pk=id)
    form = AnuncioForm(request.POST or None, instance=anuncio)
    if form.is_valid():
        form.save()
        return redirect('listar_anuncio')
    return render(request, 'anuncio/editar.html', {'form': form, 'anuncio': anuncio})


@login_required
def deletar(request, id):
    anuncio = get_object_or_404(Anuncio, pk=id)
    if request.method == 'POST':
        anuncio.delete()
        return redirect('listar_anuncio')
    return render(request, 'anuncio/deletar.html', {'anuncio': anuncio})


class AnuncioAPIView(generics.ListCreateAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer
    permission_classes = [IsAuthenticated]


class AnuncioDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Anuncio.objects.all()
    serializer_class = AnuncioSerializer
    permission_classes = [IsAuthenticated]
