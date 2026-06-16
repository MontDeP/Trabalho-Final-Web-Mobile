import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NavController, LoadingController, ToastController } from '@ionic/angular';
import { Storage } from '@ionic/storage-angular';
import { AvaliacaoService } from '../../services/avaliacao.service';
import { JogoService, Jogo } from '../../services/jogo.service';

@Component({
  selector: 'app-nova-avaliacao',
  templateUrl: 'nova-avaliacao.page.html',
  styleUrls: ['nova-avaliacao.page.scss'],
  standalone: false,
})
export class NovaAvaliacaoPage implements OnInit {
  jogos: Jogo[] = [];
  jogoSelecionado: number = 0;
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
    private jogoService: JogoService,
  ) {}

  async ngOnInit() {
    await this.storage.create();
    this.token = await this.storage.get('token');
    if (!this.token) { this.navCtrl.navigateRoot('/home'); return; }

    const jogoId = this.route.snapshot.queryParamMap.get('jogo');
    if (jogoId) { this.jogoSelecionado = Number(jogoId); }

    this.jogoService.listar(this.token).subscribe({
      next: (dados) => {
        this.jogos = dados;
        if (!this.jogoSelecionado && dados.length > 0) {
          this.jogoSelecionado = dados[0].id;
        }
      }
    });
  }

  async salvar() {
    if (!this.titulo.trim() || !this.descricao.trim() || !this.jogoSelecionado) {
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

    this.avaliacaoService.criar(this.token, {
      titulo: this.titulo,
      descricao: this.descricao,
      jogo: this.jogoSelecionado,
      nota: this.nota,
    }).subscribe({
      next: async () => {
        await loading.dismiss();
        const toast = await this.toastCtrl.create({
          message: 'Avaliação enviada com sucesso!',
          duration: 2000,
          color: 'success',
        });
        await toast.present();
        this.navCtrl.navigateBack('/avaliacoes');
      },
      error: async () => {
        await loading.dismiss();
        const toast = await this.toastCtrl.create({
          message: 'Erro ao enviar avaliação.',
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
