from django.contrib import admin
from .models import Anuncio


@admin.register(Anuncio)
class AnuncioAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'data_publicacao', 'ativo')
    list_filter = ('ativo',)
