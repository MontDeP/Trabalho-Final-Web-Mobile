import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

import { AvaliacaoService, Avaliacao } from './avaliacao.service';
import { environment } from '../../environments/environment';

const avaliacaoMock: Avaliacao = {
  id: 1,
  titulo: 'Excelente',
  descricao: 'Jogo incrível.',
  jogo: 1,
  titulo_jogo: 'God of War (PlayStation 5)',
  usuario: 1,
  nome_usuario: 'admin',
  nota: 9.5,
  criado_em: '2026-06-16T10:00:00Z',
  atualizado_em: '2026-06-16T10:00:00Z',
};

const TOKEN = 'token-teste';
const API = environment.apiUrl;

describe('AvaliacaoService', () => {
  let service: AvaliacaoService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AvaliacaoService],
    });
    service = TestBed.inject(AvaliacaoService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('deve ser criado', () => {
    expect(service).toBeTruthy();
  });

  it('listar() deve fazer GET em /avaliacao/api/ com autorização', () => {
    service.listar(TOKEN).subscribe((itens) => {
      expect(itens.length).toBe(1);
      expect(itens[0].titulo).toBe('Excelente');
    });

    const req = httpMock.expectOne(`${API}/avaliacao/api/`);
    expect(req.request.method).toBe('GET');
    expect(req.request.headers.get('Authorization')).toBe(`Token ${TOKEN}`);
    req.flush([avaliacaoMock]);
  });

  it('buscar() deve fazer GET em /avaliacao/api/<id>/', () => {
    service.buscar(TOKEN, 1).subscribe((av) => {
      expect(av.id).toBe(1);
      expect(av.nome_usuario).toBe('admin');
    });

    const req = httpMock.expectOne(`${API}/avaliacao/api/1/`);
    expect(req.request.method).toBe('GET');
    req.flush(avaliacaoMock);
  });

  it('criar() deve fazer POST em /avaliacao/api/', () => {
    const payload = { titulo: 'Nova', descricao: 'Desc', jogo: 1, nota: 8 };

    service.criar(TOKEN, payload).subscribe((av) => {
      expect(av.titulo).toBe('Nova');
    });

    const req = httpMock.expectOne(`${API}/avaliacao/api/`);
    expect(req.request.method).toBe('POST');
    expect(req.request.headers.get('Authorization')).toBe(`Token ${TOKEN}`);
    expect(req.request.body).toEqual(payload);
    req.flush({ ...avaliacaoMock, titulo: 'Nova' });
  });

  it('editar() deve fazer PATCH em /avaliacao/api/<id>/', () => {
    const payload = { titulo: 'Atualizada', descricao: 'Nova desc', nota: 7 };

    service.editar(TOKEN, 1, payload).subscribe((av) => {
      expect(av.titulo).toBe('Atualizada');
    });

    const req = httpMock.expectOne(`${API}/avaliacao/api/1/`);
    expect(req.request.method).toBe('PATCH');
    expect(req.request.body).toEqual(payload);
    req.flush({ ...avaliacaoMock, ...payload });
  });
});
