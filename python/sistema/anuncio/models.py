from django.db import models
from veiculo.models import Veiculo


class Anuncio(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    descricao = models.TextField()
    data_publicacao = models.DateField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f'Anúncio - {self.veiculo}'
