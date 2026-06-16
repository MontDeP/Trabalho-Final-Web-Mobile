from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import Jogo


def jogo_payload(**kwargs):
    dados = {
        'titulo': 'Jogo Teste',
        'plataforma': 1,
        'genero': 1,
        'ano': 2023,
        'desenvolvedor': 'Dev Teste',
    }
    dados.update(kwargs)
    return dados


class JogoAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.usuario = User.objects.create_user(username='tester', password='senha123')
        self.token = Token.objects.create(user=self.usuario)
        self.jogo = Jogo.objects.create(**jogo_payload())

    def autenticar(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    # --- Listagem (GET /jogo/api/) ---

    def test_listar_jogos_sem_autenticacao(self):
        response = self.client.get('/jogo/api/')
        self.assertEqual(response.status_code, 200)

    def test_listar_jogos_retorna_lista(self):
        response = self.client.get('/jogo/api/')
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

    def test_listar_retorna_campos_calculados(self):
        response = self.client.get('/jogo/api/')
        item = response.data[0]
        self.assertIn('nome_plataforma', item)
        self.assertIn('nome_genero', item)
        self.assertEqual(item['nome_plataforma'], 'PC')

    # --- Criação (POST /jogo/api/) ---

    def test_criar_jogo_sem_autenticacao_retorna_401(self):
        response = self.client.post('/jogo/api/', jogo_payload(), format='json')
        self.assertEqual(response.status_code, 401)

    def test_criar_jogo_com_autenticacao(self):
        self.autenticar()
        response = self.client.post('/jogo/api/', jogo_payload(titulo='Novo Jogo'), format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Jogo.objects.count(), 2)

    def test_criar_jogo_sem_titulo_retorna_400(self):
        self.autenticar()
        payload = jogo_payload()
        del payload['titulo']
        response = self.client.post('/jogo/api/', payload, format='json')
        self.assertEqual(response.status_code, 400)

    def test_criar_jogo_sem_desenvolvedor_retorna_400(self):
        self.autenticar()
        payload = jogo_payload()
        del payload['desenvolvedor']
        response = self.client.post('/jogo/api/', payload, format='json')
        self.assertEqual(response.status_code, 400)

    # --- Detalhe (GET /jogo/api/<id>/) ---

    def test_buscar_jogo_sem_autenticacao_retorna_401(self):
        response = self.client.get(f'/jogo/api/{self.jogo.pk}/')
        self.assertEqual(response.status_code, 401)

    def test_buscar_jogo_com_autenticacao(self):
        self.autenticar()
        response = self.client.get(f'/jogo/api/{self.jogo.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['titulo'], self.jogo.titulo)

    def test_buscar_jogo_inexistente_retorna_404(self):
        self.autenticar()
        response = self.client.get('/jogo/api/9999/')
        self.assertEqual(response.status_code, 404)

    # --- Edição (PATCH /jogo/api/<id>/) ---

    def test_editar_jogo_sem_autenticacao_retorna_401(self):
        response = self.client.patch(f'/jogo/api/{self.jogo.pk}/', {'titulo': 'X'}, format='json')
        self.assertEqual(response.status_code, 401)

    def test_editar_jogo_com_autenticacao(self):
        self.autenticar()
        response = self.client.patch(f'/jogo/api/{self.jogo.pk}/', {'titulo': 'Título Editado'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.jogo.refresh_from_db()
        self.assertEqual(self.jogo.titulo, 'Título Editado')

    # --- Deleção (DELETE /jogo/api/<id>/) ---

    def test_deletar_jogo_sem_autenticacao_retorna_401(self):
        response = self.client.delete(f'/jogo/api/{self.jogo.pk}/')
        self.assertEqual(response.status_code, 401)

    def test_deletar_jogo_com_autenticacao(self):
        self.autenticar()
        response = self.client.delete(f'/jogo/api/{self.jogo.pk}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Jogo.objects.count(), 0)


class JogoModelTests(TestCase):

    def test_str_retorna_titulo_e_plataforma(self):
        jogo = Jogo(**jogo_payload())
        self.assertIn('Jogo Teste', str(jogo))
        self.assertIn('PC', str(jogo))

    def test_lancamento_recente_jogo_novo(self):
        from datetime import datetime
        jogo = Jogo(**jogo_payload(ano=datetime.now().year))
        self.assertTrue(jogo.lancamento_recente)

    def test_lancamento_recente_jogo_antigo(self):
        jogo = Jogo(**jogo_payload(ano=2000))
        self.assertFalse(jogo.lancamento_recente)

    def test_anos_desde_lancamento(self):
        from datetime import datetime
        jogo = Jogo(**jogo_payload(ano=datetime.now().year - 3))
        self.assertEqual(jogo.anos_desde_lancamento(), 3)
