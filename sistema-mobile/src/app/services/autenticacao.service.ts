import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface RespostaLogin {
  id: number;
  nome: string;
  email: string;
  token: string;
}

@Injectable({ providedIn: 'root' })
export class AutenticacaoService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<RespostaLogin> {
    return this.http.post<RespostaLogin>(
      `${this.apiUrl}/autenticacao-api/`,
      { username, password }
    );
  }
}
