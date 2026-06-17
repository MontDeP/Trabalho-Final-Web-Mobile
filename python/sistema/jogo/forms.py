from django.forms import ModelForm
from django import forms
from .models import Jogo


class JogoForm(ModelForm):
    class Meta:
        model = Jogo
        fields = ['titulo', 'plataforma', 'genero', 'ano', 'desenvolvedor', 'foto']
        widgets = {
            'titulo':        forms.TextInput(attrs={'class': 'form-control'}),
            'plataforma':    forms.Select(attrs={'class': 'form-select'}),
            'genero':        forms.Select(attrs={'class': 'form-select'}),
            'ano':           forms.NumberInput(attrs={'class': 'form-control'}),
            'desenvolvedor': forms.TextInput(attrs={'class': 'form-control'}),
            'foto':          forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
