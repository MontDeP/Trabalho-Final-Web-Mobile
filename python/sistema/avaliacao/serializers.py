from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Avaliacao


class SerializadorAvaliacao(ModelSerializer):
    titulo_jogo  = SerializerMethodField()
    nome_usuario = SerializerMethodField()

    def get_titulo_jogo(self, obj):
        return str(obj.jogo)

    def get_nome_usuario(self, obj):
        return obj.usuario.username

    class Meta:
        model = Avaliacao
        fields = '__all__'
        read_only_fields = ['usuario', 'criado_em', 'atualizado_em']
