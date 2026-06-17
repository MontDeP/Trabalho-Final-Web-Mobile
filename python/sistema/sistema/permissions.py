from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Leitura livre para todos. Escrita apenas para o dono do objeto ou staff.
    Verifica o campo 'usuario' (Avaliacao) ou 'criado_por' (Jogo).
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        owner = getattr(obj, 'usuario', None) or getattr(obj, 'criado_por', None)
        return owner == request.user
