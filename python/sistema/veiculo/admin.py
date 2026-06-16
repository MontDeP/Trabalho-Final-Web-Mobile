from django.contrib import admin
from .models import Veiculo


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'ano', 'cor', 'preco')
    list_filter = ('marca', 'cor', 'combustivel')
    search_fields = ('modelo', 'marca')
