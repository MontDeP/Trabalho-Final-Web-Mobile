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
        self.jogo = Jogo.objects.create(**jogo_payload(), criado_por=self.usuario)

    def autenticar(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

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

    def test_editar_jogo_sem_autenticacao_retorna_401(self):
        response = self.client.patch(f'/jogo/api/{self.jogo.pk}/', {'titulo': 'X'}, format='json')
        self.assertEqual(response.status_code, 401)

    def test_editar_jogo_com_autenticacao(self):
        self.autenticar()
        response = self.client.patch(f'/jogo/api/{self.jogo.pk}/', {'titulo': 'Título Editado'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.jogo.refresh_from_db()
        self.assertEqual(self.jogo.titulo, 'Título Editado')

    def test_deletar_jogo_sem_autenticacao_retorna_401(self):
        response = self.client.delete(f'/jogo/api/{self.jogo.pk}/')
        self.assertEqual(response.status_code, 401)

    def test_deletar_jogo_com_autenticacao(self):
        self.autenticar()
        response = self.client.delete(f'/jogo/api/{self.jogo.pk}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Jogo.objects.count(), 0)


class JogoOwnershipTests(TestCase):

    def setUp(self):
        self.dono = User.objects.create_user(username='dono', password='senha123')
        self.outro = User.objects.create_user(username='outro', password='senha123')
        self.staff = User.objects.create_user(username='staff', password='senha123', is_staff=True)

        self.token_dono  = Token.objects.create(user=self.dono)
        self.token_outro = Token.objects.create(user=self.outro)
        self.token_staff = Token.objects.create(user=self.staff)

        self.jogo = Jogo.objects.create(**jogo_payload(), criado_por=self.dono)

    def _auth(self, token):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        return client

    def test_criar_jogo_define_criado_por_automaticamente(self):
        client = self._auth(self.token_dono)
        response = client.post('/jogo/api/', jogo_payload(titulo='Auto'), format='json')
        self.assertEqual(response.status_code, 201)
        novo = Jogo.objects.get(pk=response.data['id'])
        self.assertEqual(novo.criado_por, self.dono)

    def test_dono_pode_editar_jogo(self):
        client = self._auth(self.token_dono)
        response = client.patch(f'/jogo/api/{self.jogo.pk}/', {'titulo': 'Editado'}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_dono_pode_deletar_jogo(self):
        client = self._auth(self.token_dono)
        response = client.delete(f'/jogo/api/{self.jogo.pk}/')
        self.assertEqual(response.status_code, 204)

    def test_outro_usuario_nao_pode_editar_jogo_retorna_403(self):
        client = self._auth(self.token_outro)
        response = client.patch(f'/jogo/api/{self.jogo.pk}/', {'titulo': 'Invasão'}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_outro_usuario_nao_pode_deletar_jogo_retorna_403(self):
        client = self._auth(self.token_outro)
        response = client.delete(f'/jogo/api/{self.jogo.pk}/')
        self.assertEqual(response.status_code, 403)

    def test_staff_pode_editar_jogo_de_outro_usuario(self):
        client = self._auth(self.token_staff)
        response = client.patch(f'/jogo/api/{self.jogo.pk}/', {'titulo': 'Staff Edit'}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_staff_pode_deletar_jogo_de_outro_usuario(self):
        client = self._auth(self.token_staff)
        response = client.delete(f'/jogo/api/{self.jogo.pk}/')
        self.assertEqual(response.status_code, 204)


class JogoFiltroWebTests(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(username='u1', password='senha123')
        self.outro   = User.objects.create_user(username='u2', password='senha123')
        Jogo.objects.create(**jogo_payload(titulo='Jogo do U1'), criado_por=self.usuario)
        Jogo.objects.create(**jogo_payload(titulo='Jogo do U2'), criado_por=self.outro)
        Jogo.objects.create(**jogo_payload(titulo='Jogo Sem Dono'))

    def test_sem_filtro_retorna_todos_os_jogos(self):
        self.client.login(username='u1', password='senha123')
        response = self.client.get('/jogo/')
        self.assertEqual(len(response.context['itens']), 3)

    def test_filtro_meus_retorna_apenas_jogos_do_usuario(self):
        self.client.login(username='u1', password='senha123')
        response = self.client.get('/jogo/?meus=1')
        titulos = [j.titulo for j in response.context['itens']]
        self.assertIn('Jogo do U1', titulos)
        self.assertNotIn('Jogo do U2', titulos)
        self.assertNotIn('Jogo Sem Dono', titulos)

    def test_filtro_meus_retorna_contexto_meus_true(self):
        self.client.login(username='u1', password='senha123')
        response = self.client.get('/jogo/?meus=1')
        self.assertTrue(response.context['meus'])


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
