import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Jogo {
  id: number;
  titulo: string;
  plataforma: number;
  genero: number;
  nome_plataforma: string;
  nome_genero: string;
  ano: number;
  desenvolvedor: string;
  foto: string | null;
  foto_url: string | null;
}

export const PLATAFORMAS = [
  { value: 1, label: 'PC' },
  { value: 2, label: 'PlayStation 4' },
  { value: 3, label: 'PlayStation 5' },
  { value: 4, label: 'Xbox One' },
  { value: 5, label: 'Xbox Series X/S' },
  { value: 6, label: 'Nintendo Switch' },
  { value: 7, label: 'Mobile' },
];

export const GENEROS = [
  { value: 1, label: 'Ação' },
  { value: 2, label: 'Aventura' },
  { value: 3, label: 'RPG' },
  { value: 4, label: 'Estratégia' },
  { value: 5, label: 'Esporte' },
  { value: 6, label: 'Corrida' },
  { value: 7, label: 'Simulação' },
  { value: 8, label: 'Terror' },
  { value: 9, label: 'Puzzle' },
];

@Injectable({ providedIn: 'root' })
export class JogoService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  private headers(token: string): HttpHeaders {
    return new HttpHeaders({ 'Authorization': `Token ${token}` });
  }

  listar(token: string): Observable<Jogo[]> {
    return this.http.get<Jogo[]>(`${this.apiUrl}/jogo/api/`, { headers: this.headers(token) });
  }

  buscar(token: string, id: number): Observable<Jogo> {
    return this.http.get<Jogo>(`${this.apiUrl}/jogo/api/${id}/`, { headers: this.headers(token) });
  }

  criar(token: string, dados: FormData | Partial<Jogo>): Observable<Jogo> {
    return this.http.post<Jogo>(`${this.apiUrl}/jogo/api/`, dados, { headers: this.headers(token) });
  }

  editar(token: string, id: number, dados: FormData | Partial<Jogo>): Observable<Jogo> {
    return this.http.patch<Jogo>(`${this.apiUrl}/jogo/api/${id}/`, dados, { headers: this.headers(token) });
  }

  deletar(token: string, id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/jogo/api/${id}/`, { headers: this.headers(token) });
  }
}
