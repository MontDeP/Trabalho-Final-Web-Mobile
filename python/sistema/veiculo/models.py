from django.db import models
from .consts import MARCAS, CORES, COMBUSTIVEIS


class Veiculo(models.Model):
    marca = models.CharField(max_length=50, choices=MARCAS)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    cor = models.CharField(max_length=30, choices=CORES)
    combustivel = models.CharField(max_length=20, choices=COMBUSTIVEIS)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quilometragem = models.IntegerField()
    foto = models.ImageField(upload_to='veiculo/fotos/', null=True, blank=True)

    def __str__(self):
        return f'{self.marca} {self.modelo} ({self.ano})'
