from django.db import models
from django.contrib.auth.models import User
from jogo.models import Jogo


class Avaliacao(models.Model):
    titulo        = models.CharField(max_length=200)
    descricao     = models.TextField()
    jogo          = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    usuario       = models.ForeignKey(User, on_delete=models.CASCADE)
    nota          = models.DecimalField(max_digits=3, decimal_places=1)
    criado_em     = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
