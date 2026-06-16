# Etapa 07 — Refatorar o App Mobile (Ionic/Angular)

## Objetivo

Adaptar o app mobile para o seu domínio: trocar identidade visual, implementar a requisição de login real, e criar a tela de listagem da entidade principal consumindo a API REST.

## Status

- [ ] Concluído

## Estado Atual do App Mobile

O app mobile do professor está em `sistema-mobile/` e tem:
- Apenas a tela de `home` (login)
- Formulário de login com `username` e `password`
- Controllers injetados: LoadingController, NavController, AlertController, ToastController, Storage
- Sem requisição HTTP real implementada (apenas alert)
- Sem HttpClient configurado

## O que fazer

### 1. Atualizar metadados do app

**Arquivo:** `sistema-mobile/ionic.config.json`
```json
{
  "name": "nome-do-seu-app",
  "integrations": { "capacitor": {} },
  "type": "angular-standalone"
}
```

**Arquivo:** `sistema-mobile/package.json`
- Atualizar `"name"` para o nome do seu projeto

**Arquivo:** `sistema-mobile/src/index.html`
- Atualizar `<title>` para o nome do seu app

### 2. Configurar a URL do backend

**Arquivo:** `sistema-mobile/src/environments/environment.ts`

```typescript
export const environment = {
  production: false,
  apiUrl: 'http://127.0.0.1:8000'  // URL do seu backend Django
};
```

> **Para testar em dispositivo físico**: use o IP da sua máquina na rede local (ex: `http://192.168.1.100:8000`), não `localhost` ou `127.0.0.1`.

### 3. Criar um Service HTTP para autenticação

Crie o serviço que faz a requisição ao backend:

```bash
cd sistema-mobile
ionic generate service services/autenticacao
```

Arquivo gerado: `src/app/services/autenticacao.service.ts`

```typescript
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
```

### 4. Criar um Service para a Entidade Principal

```bash
ionic generate service services/entidade-principal
```

Arquivo: `src/app/services/entidade-principal.service.ts`

```typescript
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface EntidadePrincipal {
  id: number;
  campo1: string;
  campo2: string;
  // demais campos do seu modelo
}

@Injectable({ providedIn: 'root' })
export class EntidadePrincipalService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  listar(token: string): Observable<EntidadePrincipal[]> {
    const headers = new HttpHeaders({
      'Authorization': `Token ${token}`
    });
    return this.http.get<EntidadePrincipal[]>(
      `${this.apiUrl}/ENTIDADE_PRINCIPAL/api/`,
      { headers }
    );
  }
}
```

### 5. Atualizar o `app.component.ts` para incluir HttpClient

**Arquivo:** `sistema-mobile/src/app/app.component.ts`

```typescript
import { Component } from '@angular/core';
import { IonApp, IonRouterOutlet } from '@ionic/angular/standalone';
import { provideHttpClient } from '@angular/common/http';  // se necessário

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  standalone: true,
  imports: [IonApp, IonRouterOutlet],
})
export class AppComponent {}
```

**Arquivo:** `sistema-mobile/src/main.ts`

Adicione `provideHttpClient()` nos providers:

```typescript
import { bootstrapApplication } from '@angular/platform-browser';
import { RouteReuseStrategy, provideRouter } from '@angular/router';
import { IonicRouteStrategy, provideIonicAngular } from '@ionic/angular/standalone';
import { provideHttpClient } from '@angular/common/http';

import { routes } from './app/app.routes';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, {
  providers: [
    { provide: RouteReuseStrategy, useClass: IonicRouteStrategy },
    provideIonicAngular(),
    provideRouter(routes),
    provideHttpClient(),  // <-- ADICIONAR
  ],
});
```

### 6. Implementar a requisição HTTP real no `home.page.ts`

**Arquivo:** `sistema-mobile/src/app/home/home.page.ts`

```typescript
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { IonContent, IonList, IonItem, IonInput, IonButton,
         IonInputPasswordToggle, LoadingController,
         NavController, AlertController, ToastController } from '@ionic/angular/standalone';
import { Storage } from '@ionic/storage-angular';
import { AutenticacaoService } from '../services/autenticacao.service';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  standalone: true,
  imports: [
    IonContent, IonList, IonItem, IonInput, IonButton,
    IonInputPasswordToggle, FormsModule
  ],
})
export class HomePage implements OnInit {
  username: string = '';
  password: string = '';

  constructor(
    private loadingCtrl: LoadingController,
    private navCtrl: NavController,
    private alertCtrl: AlertController,
    private toastCtrl: ToastController,
    private storage: Storage,
    private autenticacaoService: AutenticacaoService,
  ) {}

  async ngOnInit() {
    await this.storage.create();
  }

  async autenticarUsuario() {
    const loading = await this.loadingCtrl.create({ message: 'Autenticando...' });
    await loading.present();

    this.autenticacaoService.login(this.username, this.password).subscribe({
      next: async (resposta) => {
        await loading.dismiss();
        await this.storage.set('token', resposta.token);
        await this.storage.set('usuario', resposta);
        this.navCtrl.navigateRoot('/lista');  // adaptar para sua rota
      },
      error: async (erro) => {
        await loading.dismiss();
        const alert = await this.alertCtrl.create({
          header: 'Erro',
          message: 'Usuário ou senha inválidos.',
          buttons: ['OK']
        });
        await alert.present();
      }
    });
  }
}
```

### 7. Criar a página de listagem da Entidade Principal

```bash
ionic generate page pages/lista
```

Isso cria `src/app/pages/lista/`:
- `lista.page.ts`
- `lista.page.html`
- `lista.page.scss`

**Arquivo:** `src/app/pages/lista/lista.page.ts`

```typescript
import { Component, OnInit } from '@angular/core';
import { NgFor, NgIf } from '@angular/common';
import { IonContent, IonList, IonItem, IonLabel,
         IonHeader, IonToolbar, IonTitle, IonButton } from '@ionic/angular/standalone';
import { Storage } from '@ionic/storage-angular';
import { EntidadePrincipalService, EntidadePrincipal } from '../../services/entidade-principal.service';

@Component({
  selector: 'app-lista',
  templateUrl: 'lista.page.html',
  standalone: true,
  imports: [
    IonContent, IonList, IonItem, IonLabel,
    IonHeader, IonToolbar, IonTitle, IonButton,
    NgFor, NgIf
  ],
})
export class ListaPage implements OnInit {
  itens: EntidadePrincipal[] = [];

  constructor(
    private storage: Storage,
    private entidadeService: EntidadePrincipalService,
  ) {}

  async ngOnInit() {
    await this.storage.create();
    const token = await this.storage.get('token');
    this.entidadeService.listar(token).subscribe({
      next: (dados) => { this.itens = dados; },
      error: (erro) => { console.error('Erro ao carregar:', erro); }
    });
  }
}
```

**Arquivo:** `src/app/pages/lista/lista.page.html`

```html
<ion-header>
  <ion-toolbar>
    <ion-title>Lista de [Entidade]</ion-title>
  </ion-toolbar>
</ion-header>

<ion-content>
  <ion-list>
    <ion-item *ngFor="let item of itens">
      <ion-label>
        <h2>{{ item.campo1 }}</h2>
        <p>{{ item.campo2 }}</p>
      </ion-label>
    </ion-item>
  </ion-list>
</ion-content>
```

### 8. Atualizar as rotas do app mobile

**Arquivo:** `sistema-mobile/src/app/app.routes.ts`

```typescript
import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: 'home',
    loadComponent: () => import('./home/home.page').then(m => m.HomePage),
  },
  {
    path: 'lista',
    loadComponent: () => import('./pages/lista/lista.page').then(m => m.ListaPage),
  },
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full',
  },
];
```

## Verificação

```bash
cd sistema-mobile
ionic serve
```

Fluxo de teste:
1. Abrir `http://localhost:8100`
2. Digitar username e senha de um usuário existente no Django
3. Verificar se navega para a lista
4. Verificar se os dados aparecem na lista

## Identidade Visual

Atualize as cores do tema Ionic:

**Arquivo:** `sistema-mobile/src/theme/variables.scss`

```scss
:root {
  --ion-color-primary: #SUA_COR_PRIMARIA;
  --ion-color-primary-rgb: R,G,B;
  // ...
}
```

## O que NÃO fazer nesta etapa

- Não implemente edição/exclusão no mobile (não foi ensinado ainda)
- Mantenha a simplicidade — listagem e login são suficientes para o escopo

## Próxima Etapa

[Etapa 08 — Limpeza Final e Revisão](08-etapa-limpeza-final.md)
