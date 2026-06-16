import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { EditarPage } from './editar.page';
import { EditarPageRoutingModule } from './editar-routing.module';

@NgModule({
  imports: [CommonModule, FormsModule, IonicModule, EditarPageRoutingModule],
  declarations: [EditarPage],
})
export class EditarPageModule {}
