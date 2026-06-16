import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NavController, LoadingController, ToastController } from '@ionic/angular';
import { Storage } from '@ionic/storage-angular';
import { AvaliacaoService } from '../../services/avaliacao.service';

@Component({
  selector: 'app-editar-avaliacao',
  templateUrl: 'editar-avaliacao.page.html',
  styleUrls: ['editar-avaliacao.page.scss'],
  standalone: false,
})
export class EditarAvaliacaoPage implements OnInit {
  id: number = 0;
  tituloJogo = '';
  titulo = '';
  descricao = '';
  nota: number = 8;

  private token = '';

  constructor(
    private route: ActivatedRoute,
    private navCtrl: NavController,
    private loadingCtrl: LoadingController,
    private toastCtrl: ToastController,
    private storage: Storage,
    private avaliacaoService: AvaliacaoService,
  ) {}

  async ngOnInit() {
    await this.storage.create();
    this.token = await this.storage.get('token');
    if (!this.token) { this.navCtrl.navigateRoot('/home'); return; }

    this.id = Number(this.route.snapshot.paramMap.get('id'));

    this.avaliacaoService.buscar(this.token, this.id).subscribe({
      next: (av) => {
        this.tituloJogo = av.titulo_jogo;
        this.titulo = av.titulo;
        this.descricao = av.descricao;
        this.nota = av.nota;
      },
      error: async () => {
        const toast = await this.toastCtrl.create({
          message: 'Erro ao carregar avaliação.',
          duration: 2000,
          color: 'danger',
        });
        await toast.present();
        this.navCtrl.navigateBack('/avaliacoes');
      }
    });
  }

  async salvar() {
    if (!this.titulo.trim() || !this.descricao.trim()) {
      const toast = await this.toastCtrl.create({
        message: 'Preencha todos os campos.',
        duration: 2000,
        color: 'warning',
      });
      await toast.present();
      return;
    }

    const loading = await this.loadingCtrl.create({ message: 'Salvando...' });
    await loading.present();

    this.avaliacaoService.editar(this.token, this.id, {
      titulo: this.titulo,
      descricao: this.descricao,
      nota: this.nota,
    }).subscribe({
      next: async () => {
        await loading.dismiss();
        const toast = await this.toastCtrl.create({
          message: 'Avaliação atualizada!',
          duration: 2000,
          color: 'success',
        });
        await toast.present();
        this.navCtrl.navigateBack('/avaliacoes');
      },
      error: async () => {
        await loading.dismiss();
        const toast = await this.toastCtrl.create({
          message: 'Erro ao salvar avaliação.',
          duration: 2000,
          color: 'danger',
        });
        await toast.present();
      }
    });
  }

  cancelar() {
    this.navCtrl.navigateBack('/avaliacoes');
  }
}
