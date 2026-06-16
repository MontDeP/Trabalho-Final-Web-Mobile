import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

import { AutenticacaoService, RespostaLogin } from './autenticacao.service';
import { environment } from '../../environments/environment';

const API = environment.apiUrl;

const respostaMock: RespostaLogin = {
  id: 1,
  nome: 'Admin',
  email: 'admin@example.com',
  token: 'abc123token',
};

describe('AutenticacaoService', () => {
  let service: AutenticacaoService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AutenticacaoService],
    });
    service = TestBed.inject(AutenticacaoService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('deve ser criado', () => {
    expect(service).toBeTruthy();
  });

  it('login() deve fazer POST em /autenticacao-api/ com username e password', () => {
    service.login('admin', 'senha123').subscribe((resposta) => {
      expect(resposta.token).toBe('abc123token');
      expect(resposta.id).toBe(1);
    });

    const req = httpMock.expectOne(`${API}/autenticacao-api/`);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual({ username: 'admin', password: 'senha123' });
    req.flush(respostaMock);
  });

  it('login() deve retornar os campos id, nome, email e token', () => {
    service.login('admin', 'senha123').subscribe((resposta) => {
      expect(resposta.id).toBeDefined();
      expect(resposta.nome).toBeDefined();
      expect(resposta.email).toBeDefined();
      expect(resposta.token).toBeDefined();
    });

    const req = httpMock.expectOne(`${API}/autenticacao-api/`);
    req.flush(respostaMock);
  });

  it('login() deve propagar erro 401 quando credenciais forem inválidas', () => {
    let erroRecebido = false;

    service.login('errado', 'errado').subscribe({
      next: () => fail('deveria ter falhado'),
      error: (err) => {
        erroRecebido = true;
        expect(err.status).toBe(401);
      },
    });

    const req = httpMock.expectOne(`${API}/autenticacao-api/`);
    req.flush({ detail: 'Invalid credentials' }, { status: 401, statusText: 'Unauthorized' });
    expect(erroRecebido).toBeTrue();
  });
});
