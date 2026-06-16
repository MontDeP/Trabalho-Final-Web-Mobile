from django.forms import ModelForm
from .models import Avaliacao


class AvaliacaoForm(ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['titulo', 'descricao', 'jogo', 'nota']
        # 'usuario' é associado automaticamente na view via form_valid
