import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { AvaliacoesPage } from './avaliacoes.page';
import { AvaliacoesPageRoutingModule } from './avaliacoes-routing.module';

@NgModule({
  imports: [CommonModule, IonicModule, AvaliacoesPageRoutingModule],
  declarations: [AvaliacoesPage],
})
export class AvaliacoesPageModule {}
