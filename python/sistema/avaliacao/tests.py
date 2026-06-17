from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from jogo.models import Jogo
from .models import Avaliacao


def criar_jogo():
    return Jogo.objects.create(
        titulo='Jogo Base',
        plataforma=1,
        genero=1,
        ano=2022,
        desenvolvedor='Dev Base',
    )


def avaliacao_payload(jogo, **kwargs):
    dados = {
        'titulo': 'Ótimo jogo',
        'descricao': 'Gostei muito desse jogo.',
        'jogo': jogo.pk,
        'nota': 9.0,
    }
    dados.update(kwargs)
    return dados


class AvaliacaoAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.usuario = User.objects.create_user(username='tester', password='senha123')
        self.token = Token.objects.create(user=self.usuario)
        self.jogo = criar_jogo()
        self.avaliacao = Avaliacao.objects.create(
            titulo='Avaliação Base',
            descricao='Descrição base.',
            jogo=self.jogo,
            usuario=self.usuario,
            nota=8.0,
        )

    def autenticar(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_listar_avaliacoes_sem_autenticacao(self):
        response = self.client.get('/avaliacao/api/')
        self.assertEqual(response.status_code, 200)

    def test_listar_avaliacoes_retorna_lista(self):
        response = self.client.get('/avaliacao/api/')
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

    def test_listar_retorna_campos_calculados(self):
        response = self.client.get('/avaliacao/api/')
        item = response.data[0]
        self.assertIn('titulo_jogo', item)
        self.assertIn('nome_usuario', item)
        self.assertEqual(item['nome_usuario'], 'tester')
        self.assertEqual(item['titulo_jogo'], str(self.jogo))

    def test_criar_avaliacao_sem_autenticacao_retorna_401(self):
        response = self.client.post('/avaliacao/api/', avaliacao_payload(self.jogo), format='json')
        self.assertEqual(response.status_code, 401)

    def test_criar_avaliacao_com_autenticacao(self):
        self.autenticar()
        response = self.client.post('/avaliacao/api/', avaliacao_payload(self.jogo), format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Avaliacao.objects.count(), 2)

    def test_criar_avaliacao_usuario_preenchido_automaticamente(self):
        self.autenticar()
        response = self.client.post('/avaliacao/api/', avaliacao_payload(self.jogo), format='json')
        self.assertEqual(response.status_code, 201)
        nova = Avaliacao.objects.get(pk=response.data['id'])
        self.assertEqual(nova.usuario, self.usuario)

    def test_criar_avaliacao_sem_titulo_retorna_400(self):
        self.autenticar()
        payload = avaliacao_payload(self.jogo)
        del payload['titulo']
        response = self.client.post('/avaliacao/api/', payload, format='json')
        self.assertEqual(response.status_code, 400)

    def test_criar_avaliacao_nota_invalida_retorna_400(self):
        self.autenticar()
        payload = avaliacao_payload(self.jogo, nota=999)
        response = self.client.post('/avaliacao/api/', payload, format='json')
        self.assertEqual(response.status_code, 400)

    def test_buscar_avaliacao_sem_autenticacao_retorna_401(self):
        response = self.client.get(f'/avaliacao/api/{self.avaliacao.pk}/')
        self.assertEqual(response.status_code, 401)

    def test_buscar_avaliacao_com_autenticacao(self):
        self.autenticar()
        response = self.client.get(f'/avaliacao/api/{self.avaliacao.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['titulo'], self.avaliacao.titulo)

    def test_buscar_avaliacao_inexistente_retorna_404(self):
        self.autenticar()
        response = self.client.get('/avaliacao/api/9999/')
        self.assertEqual(response.status_code, 404)

    def test_editar_avaliacao_sem_autenticacao_retorna_401(self):
        response = self.client.patch(f'/avaliacao/api/{self.avaliacao.pk}/', {'titulo': 'X'}, format='json')
        self.assertEqual(response.status_code, 401)

    def test_editar_avaliacao_com_autenticacao(self):
        self.autenticar()
        response = self.client.patch(
            f'/avaliacao/api/{self.avaliacao.pk}/',
            {'titulo': 'Título Atualizado', 'nota': 7.5},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.avaliacao.refresh_from_db()
        self.assertEqual(self.avaliacao.titulo, 'Título Atualizado')
        self.assertEqual(float(self.avaliacao.nota), 7.5)

    def test_deletar_avaliacao_sem_autenticacao_retorna_401(self):
        response = self.client.delete(f'/avaliacao/api/{self.avaliacao.pk}/')
        self.assertEqual(response.status_code, 401)

    def test_deletar_avaliacao_com_autenticacao(self):
        self.autenticar()
        response = self.client.delete(f'/avaliacao/api/{self.avaliacao.pk}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Avaliacao.objects.count(), 0)


class AvaliacaoOwnershipTests(TestCase):

    def setUp(self):
        self.dono  = User.objects.create_user(username='dono',  password='senha123')
        self.outro = User.objects.create_user(username='outro', password='senha123')
        self.staff = User.objects.create_user(username='staff', password='senha123', is_staff=True)

        self.token_dono  = Token.objects.create(user=self.dono)
        self.token_outro = Token.objects.create(user=self.outro)
        self.token_staff = Token.objects.create(user=self.staff)

        self.jogo = criar_jogo()
        self.avaliacao = Avaliacao.objects.create(
            titulo='Avaliação do Dono',
            descricao='Desc.',
            jogo=self.jogo,
            usuario=self.dono,
            nota=8.0,
        )

    def _auth(self, token):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        return client

    def test_dono_pode_editar_avaliacao(self):
        client = self._auth(self.token_dono)
        response = client.patch(f'/avaliacao/api/{self.avaliacao.pk}/', {'titulo': 'Editada'}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_dono_pode_deletar_avaliacao(self):
        client = self._auth(self.token_dono)
        response = client.delete(f'/avaliacao/api/{self.avaliacao.pk}/')
        self.assertEqual(response.status_code, 204)

    def test_outro_usuario_nao_pode_editar_avaliacao_retorna_403(self):
        client = self._auth(self.token_outro)
        response = client.patch(f'/avaliacao/api/{self.avaliacao.pk}/', {'titulo': 'Invasão'}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_outro_usuario_nao_pode_deletar_avaliacao_retorna_403(self):
        client = self._auth(self.token_outro)
        response = client.delete(f'/avaliacao/api/{self.avaliacao.pk}/')
        self.assertEqual(response.status_code, 403)

    def test_staff_pode_editar_avaliacao_de_outro_usuario(self):
        client = self._auth(self.token_staff)
        response = client.patch(f'/avaliacao/api/{self.avaliacao.pk}/', {'titulo': 'Staff Edit'}, format='json')
        self.assertEqual(response.status_code, 200)

    def test_staff_pode_deletar_avaliacao_de_outro_usuario(self):
        client = self._auth(self.token_staff)
        response = client.delete(f'/avaliacao/api/{self.avaliacao.pk}/')
        self.assertEqual(response.status_code, 204)


class AvaliacaoFiltroWebTests(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(username='u1', password='senha123')
        self.outro   = User.objects.create_user(username='u2', password='senha123')
        jogo = criar_jogo()
        Avaliacao.objects.create(titulo='AV U1', descricao='', jogo=jogo, usuario=self.usuario, nota=9.0)
        Avaliacao.objects.create(titulo='AV U2', descricao='', jogo=jogo, usuario=self.outro,   nota=7.0)

    def test_sem_filtro_retorna_todas_as_avaliacoes(self):
        self.client.login(username='u1', password='senha123')
        response = self.client.get('/avaliacao/')
        self.assertEqual(len(response.context['itens']), 2)

    def test_filtro_minhas_retorna_apenas_avaliacoes_do_usuario(self):
        self.client.login(username='u1', password='senha123')
        response = self.client.get('/avaliacao/?minhas=1')
        titulos = [av.titulo for av in response.context['itens']]
        self.assertIn('AV U1', titulos)
        self.assertNotIn('AV U2', titulos)

    def test_filtro_minhas_retorna_contexto_minhas_true(self):
        self.client.login(username='u1', password='senha123')
        response = self.client.get('/avaliacao/?minhas=1')
        self.assertTrue(response.context['minhas'])


class AvaliacaoModelTests(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(username='u', password='p')
        self.jogo = criar_jogo()

    def test_str_retorna_titulo(self):
        av = Avaliacao(
            titulo='Minha Avaliação',
            descricao='Desc.',
            jogo=self.jogo,
            usuario=self.usuario,
            nota=9.0,
        )
        self.assertEqual(str(av), 'Minha Avaliação')

    def test_cascade_deleta_avaliacao_com_jogo(self):
        Avaliacao.objects.create(
            titulo='AV',
            descricao='Desc',
            jogo=self.jogo,
            usuario=self.usuario,
            nota=5.0,
        )
        self.assertEqual(Avaliacao.objects.count(), 1)
        self.jogo.delete()
        self.assertEqual(Avaliacao.objects.count(), 0)
