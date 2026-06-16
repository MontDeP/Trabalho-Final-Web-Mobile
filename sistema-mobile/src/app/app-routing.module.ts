import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'home',
    loadChildren: () => import('./home/home.module').then(m => m.HomePageModule)
  },
  {
    path: 'lista',
    loadChildren: () => import('./pages/lista/lista.module').then(m => m.ListaPageModule)
  },
  {
    path: 'editar/:id',
    loadChildren: () => import('./pages/editar/editar.module').then(m => m.EditarPageModule)
  },
  {
    path: 'novo',
    loadChildren: () => import('./pages/novo/novo.module').then(m => m.NovoPageModule)
  },
  {
    path: 'avaliacoes',
    loadChildren: () => import('./pages/avaliacoes/avaliacoes.module').then(m => m.AvaliacoesPageModule)
  },
  {
    path: 'nova-avaliacao',
    loadChildren: () => import('./pages/nova-avaliacao/nova-avaliacao.module').then(m => m.NovaAvaliacaoPageModule)
  },
  {
    path: 'editar-avaliacao/:id',
    loadChildren: () => import('./pages/editar-avaliacao/editar-avaliacao.module').then(m => m.EditarAvaliacaoPageModule)
  },
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule {}
