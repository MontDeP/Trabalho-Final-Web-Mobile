from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Veiculo
from .forms import VeiculoForm
from .serializers import VeiculoSerializer


@login_required
def listar(request):
    veiculos = Veiculo.objects.all()
    return render(request, 'veiculo/listar.html', {'veiculos': veiculos})


@login_required
def novo(request):
    form = VeiculoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('listar_veiculo')
    return render(request, 'veiculo/novo.html', {'form': form})


@login_required
def editar(request, id):
    veiculo = get_object_or_404(Veiculo, pk=id)
    form = VeiculoForm(request.POST or None, request.FILES or None, instance=veiculo)
    if form.is_valid():
        form.save()
        return redirect('listar_veiculo')
    return render(request, 'veiculo/editar.html', {'form': form, 'veiculo': veiculo})


@login_required
def deletar(request, id):
    veiculo = get_object_or_404(Veiculo, pk=id)
    if request.method == 'POST':
        veiculo.delete()
        return redirect('listar_veiculo')
    return render(request, 'veiculo/deletar.html', {'veiculo': veiculo})


class VeiculoAPIView(generics.ListCreateAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    permission_classes = [IsAuthenticated]


class VeiculoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    permission_classes = [IsAuthenticated]
