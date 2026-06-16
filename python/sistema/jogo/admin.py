from django.contrib import admin
from .models import Jogo


@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'get_plataforma_display', 'get_genero_display', 'ano', 'criado_em']
    list_filter = ['plataforma', 'genero']
    search_fields = ['titulo', 'desenvolvedor']
