from django.contrib import admin
from .models import Avaliacao


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'jogo', 'usuario', 'nota', 'criado_em']
    list_filter = ['nota']
    search_fields = ['titulo', 'jogo__titulo']
