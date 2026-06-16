from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('listar_jogos')
        return render(request, 'autenticacao.html')

    def post(self, request):
        username = request.POST.get('usuario')
        password = request.POST.get('senha')
        usuario = authenticate(request, username=username, password=password)
        if usuario:
            login(request, usuario)
            return redirect('listar_jogos')
        return render(request, 'autenticacao.html', {'erro': 'Usuário ou senha inválidos'})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class LoginAPI(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id': user.pk,
            'nome': user.get_full_name(),
            'email': user.email,
            'token': token.key
        })
