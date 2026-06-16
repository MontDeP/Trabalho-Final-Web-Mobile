import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { NovaAvaliacaoPage } from './nova-avaliacao.page';
import { NovaAvaliacaoPageRoutingModule } from './nova-avaliacao-routing.module';

@NgModule({
  imports: [CommonModule, FormsModule, IonicModule, NovaAvaliacaoPageRoutingModule],
  declarations: [NovaAvaliacaoPage],
})
export class NovaAvaliacaoPageModule {}
