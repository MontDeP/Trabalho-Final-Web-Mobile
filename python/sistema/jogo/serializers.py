from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Jogo


class SerializadorJogo(ModelSerializer):
    nome_plataforma = SerializerMethodField()
    nome_genero     = SerializerMethodField()
    foto_url        = SerializerMethodField()

    def get_nome_plataforma(self, obj):
        return obj.get_plataforma_display()

    def get_nome_genero(self, obj):
        return obj.get_genero_display()

    def get_foto_url(self, obj):
        if not obj.foto:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.foto.url)
        return obj.foto.url

    class Meta:
        model = Jogo
        fields = '__all__'
