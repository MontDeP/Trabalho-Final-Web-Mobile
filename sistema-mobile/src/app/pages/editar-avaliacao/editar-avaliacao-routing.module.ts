import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EditarAvaliacaoPage } from './editar-avaliacao.page';

const routes: Routes = [
  { path: '', component: EditarAvaliacaoPage }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class EditarAvaliacaoPageRoutingModule {}
