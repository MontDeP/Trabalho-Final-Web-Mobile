import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { EditarAvaliacaoPage } from './editar-avaliacao.page';
import { EditarAvaliacaoPageRoutingModule } from './editar-avaliacao-routing.module';

@NgModule({
  imports: [CommonModule, FormsModule, IonicModule, EditarAvaliacaoPageRoutingModule],
  declarations: [EditarAvaliacaoPage],
})
export class EditarAvaliacaoPageModule {}
