import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

import { JogoService, Jogo } from './jogo.service';
import { environment } from '../../environments/environment';

const jogoMock: Jogo = {
  id: 1,
  titulo: 'God of War',
  plataforma: 3,
  genero: 1,
  nome_plataforma: 'PlayStation 5',
  nome_genero: 'Ação',
  ano: 2022,
  desenvolvedor: 'Santa Monica Studio',
  foto: null,
  foto_url: null,
};

const TOKEN = 'token-teste';
const API = environment.apiUrl;

describe('JogoService', () => {
  let service: JogoService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [JogoService],
    });
    service = TestBed.inject(JogoService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('deve ser criado', () => {
    expect(service).toBeTruthy();
  });

  it('listar() deve fazer GET em /jogo/api/ com header de autorização', () => {
    service.listar(TOKEN).subscribe((jogos) => {
      expect(jogos.length).toBe(1);
      expect(jogos[0].titulo).toBe('God of War');
    });

    const req = httpMock.expectOne(`${API}/jogo/api/`);
    expect(req.request.method).toBe('GET');
    expect(req.request.headers.get('Authorization')).toBe(`Token ${TOKEN}`);
    req.flush([jogoMock]);
  });

  it('buscar() deve fazer GET em /jogo/api/<id>/', () => {
    service.buscar(TOKEN, 1).subscribe((jogo) => {
      expect(jogo.id).toBe(1);
    });

    const req = httpMock.expectOne(`${API}/jogo/api/1/`);
    expect(req.request.method).toBe('GET');
    req.flush(jogoMock);
  });

  it('criar() deve fazer POST em /jogo/api/', () => {
    const payload = { titulo: 'Novo Jogo', plataforma: 1, genero: 1, ano: 2024, desenvolvedor: 'Dev' };

    service.criar(TOKEN, payload).subscribe((jogo) => {
      expect(jogo.titulo).toBe('Novo Jogo');
    });

    const req = httpMock.expectOne(`${API}/jogo/api/`);
    expect(req.request.method).toBe('POST');
    expect(req.request.headers.get('Authorization')).toBe(`Token ${TOKEN}`);
    req.flush({ ...jogoMock, titulo: 'Novo Jogo' });
  });

  it('editar() deve fazer PATCH em /jogo/api/<id>/', () => {
    service.editar(TOKEN, 1, { titulo: 'Editado' }).subscribe((jogo) => {
      expect(jogo.titulo).toBe('Editado');
    });

    const req = httpMock.expectOne(`${API}/jogo/api/1/`);
    expect(req.request.method).toBe('PATCH');
    expect(req.request.body).toEqual({ titulo: 'Editado' });
    req.flush({ ...jogoMock, titulo: 'Editado' });
  });

  it('deletar() deve fazer DELETE em /jogo/api/<id>/', () => {
    service.deletar(TOKEN, 1).subscribe((res) => {
      expect(res).toBeNull();
    });

    const req = httpMock.expectOne(`${API}/jogo/api/1/`);
    expect(req.request.method).toBe('DELETE');
    req.flush(null);
  });
});
