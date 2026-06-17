from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class LoginAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.usuario = User.objects.create_user(
            username='admin',
            password='senha123',
            first_name='Admin',
            last_name='User',
            email='admin@example.com',
        )

    def test_login_com_credenciais_validas_retorna_200(self):
        response = self.client.post('/autenticacao-api/', {
            'username': 'admin',
            'password': 'senha123',
        }, format='json')
        self.assertEqual(response.status_code, 200)

    def test_login_retorna_token(self):
        response = self.client.post('/autenticacao-api/', {
            'username': 'admin',
            'password': 'senha123',
        }, format='json')
        self.assertIn('token', response.data)
        self.assertTrue(len(response.data['token']) > 0)

    def test_login_retorna_campos_id_nome_email(self):
        response = self.client.post('/autenticacao-api/', {
            'username': 'admin',
            'password': 'senha123',
        }, format='json')
        self.assertIn('id', response.data)
        self.assertIn('nome', response.data)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['id'], self.usuario.pk)
        self.assertEqual(response.data['email'], 'admin@example.com')

    def test_login_cria_token_no_banco(self):
        self.client.post('/autenticacao-api/', {
            'username': 'admin',
            'password': 'senha123',
        }, format='json')
        self.assertTrue(Token.objects.filter(user=self.usuario).exists())

    def test_login_mesmo_token_em_chamadas_repetidas(self):
        r1 = self.client.post('/autenticacao-api/', {'username': 'admin', 'password': 'senha123'}, format='json')
        r2 = self.client.post('/autenticacao-api/', {'username': 'admin', 'password': 'senha123'}, format='json')
        self.assertEqual(r1.data['token'], r2.data['token'])

    def test_login_com_senha_errada_retorna_400(self):
        response = self.client.post('/autenticacao-api/', {
            'username': 'admin',
            'password': 'senhaerrada',
        }, format='json')
        self.assertEqual(response.status_code, 400)

    def test_login_com_usuario_inexistente_retorna_400(self):
        response = self.client.post('/autenticacao-api/', {
            'username': 'naoexiste',
            'password': 'qualquer',
        }, format='json')
        self.assertEqual(response.status_code, 400)

    def test_login_sem_campos_retorna_400(self):
        response = self.client.post('/autenticacao-api/', {}, format='json')
        self.assertEqual(response.status_code, 400)
