import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Avaliacao {
  id: number;
  titulo: string;
  descricao: string;
  jogo: number;
  titulo_jogo: string;
  usuario: number;
  nome_usuario: string;
  nota: number;
  criado_em: string;
  atualizado_em: string;
}

@Injectable({ providedIn: 'root' })
export class AvaliacaoService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  private headers(token: string): HttpHeaders {
    return new HttpHeaders({ 'Authorization': `Token ${token}` });
  }

  listar(token: string): Observable<Avaliacao[]> {
    return this.http.get<Avaliacao[]>(`${this.apiUrl}/avaliacao/api/`, { headers: this.headers(token) });
  }

  buscar(token: string, id: number): Observable<Avaliacao> {
    return this.http.get<Avaliacao>(`${this.apiUrl}/avaliacao/api/${id}/`, { headers: this.headers(token) });
  }

  criar(token: string, dados: { titulo: string; descricao: string; jogo: number; nota: number }): Observable<Avaliacao> {
    return this.http.post<Avaliacao>(`${this.apiUrl}/avaliacao/api/`, dados, { headers: this.headers(token) });
  }

  editar(token: string, id: number, dados: { titulo: string; descricao: string; nota: number }): Observable<Avaliacao> {
    return this.http.patch<Avaliacao>(`${this.apiUrl}/avaliacao/api/${id}/`, dados, { headers: this.headers(token) });
  }
}
