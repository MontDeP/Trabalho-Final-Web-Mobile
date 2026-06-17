import { Component, OnInit } from '@angular/core';
import { NavController, AlertController, ToastController } from '@ionic/angular';
import { Storage } from '@ionic/storage-angular';
import { JogoService, Jogo } from '../../services/jogo.service';

@Component({
  selector: 'app-lista',
  templateUrl: 'lista.page.html',
  styleUrls: ['lista.page.scss'],
  standalone: false,
})
export class ListaPage implements OnInit {
  itens: Jogo[] = [];
  carregando = true;
  usuarioId: number | null = null;
  mostrarMeus = false;
  private token = '';

  get itensFiltrados(): Jogo[] {
    if (this.mostrarMeus) {
      return this.itens.filter(j => j.criado_por === this.usuarioId);
    }
    return this.itens;
  }

  constructor(
    private storage: Storage,
    private jogoService: JogoService,
    private navCtrl: NavController,
    private alertCtrl: AlertController,
    private toastCtrl: ToastController,
  ) {}

  async ngOnInit() {
    await this.storage.create();
    this.token = await this.storage.get('token');
    if (!this.token) {
      this.navCtrl.navigateRoot('/home');
      return;
    }
    const usuario = await this.storage.get('usuario');
    if (usuario) { this.usuarioId = usuario.id; }
    this.carregarJogos();
  }

  carregarJogos() {
    this.carregando = true;
    this.jogoService.listar(this.token).subscribe({
      next: (dados) => { this.itens = dados; this.carregando = false; },
      error: () => { this.carregando = false; }
    });
  }

  toggleMeus() {
    this.mostrarMeus = !this.mostrarMeus;
  }

  verAvaliacoes() {
    this.navCtrl.navigateForward('/avaliacoes');
  }

  novoJogo() {
    this.navCtrl.navigateForward('/novo');
  }

  editarJogo(id: number) {
    this.navCtrl.navigateForward(`/editar/${id}`);
  }

  avaliarJogo(id: number) {
    this.navCtrl.navigateForward('/nova-avaliacao', { queryParams: { jogo: id } });
  }

  async confirmarDelete(jogo: Jogo) {
    const alert = await this.alertCtrl.create({
      header: 'Excluir Jogo',
      message: `Tem certeza que deseja excluir "${jogo.titulo}"?`,
      buttons: [
        { text: 'Cancelar', role: 'cancel' },
        {
          text: 'Excluir',
          role: 'destructive',
          handler: () => this.deletarJogo(jogo.id),
        },
      ],
    });
    await alert.present();
  }

  deletarJogo(id: number) {
    this.jogoService.deletar(this.token, id).subscribe({
      next: async () => {
        this.itens = this.itens.filter(j => j.id !== id);
        const toast = await this.toastCtrl.create({
          message: 'Jogo excluído com sucesso.',
          duration: 2000,
          color: 'success',
        });
        await toast.present();
      },
      error: async () => {
        const toast = await this.toastCtrl.create({
          message: 'Erro ao excluir o jogo.',
          duration: 2000,
          color: 'danger',
        });
        await toast.present();
      }
    });
  }

  async sair() {
    await this.storage.remove('token');
    await this.storage.remove('usuario');
    this.navCtrl.navigateRoot('/home');
  }
}
