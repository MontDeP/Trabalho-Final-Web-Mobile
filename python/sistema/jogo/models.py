from datetime import datetime
from django.db import models
from .consts import PLATAFORMAS, GENEROS


class Jogo(models.Model):
    titulo        = models.CharField(max_length=150)
    plataforma    = models.SmallIntegerField(choices=PLATAFORMAS)
    genero        = models.SmallIntegerField(choices=GENEROS)
    ano           = models.IntegerField()
    desenvolvedor = models.CharField(max_length=100)
    foto          = models.ImageField(upload_to='jogo/fotos', null=True, blank=True)
    criado_em     = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.titulo} ({self.get_plataforma_display()})'

    @property
    def lancamento_recente(self):
        return self.ano >= datetime.now().year - 2

    def anos_desde_lancamento(self):
        return datetime.now().year - self.ano
