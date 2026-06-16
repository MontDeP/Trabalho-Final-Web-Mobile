import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { ListaPage } from './lista.page';
import { ListaPageRoutingModule } from './lista-routing.module';

@NgModule({
  imports: [CommonModule, IonicModule, ListaPageRoutingModule],
  declarations: [ListaPage],
})
export class ListaPageModule {}
