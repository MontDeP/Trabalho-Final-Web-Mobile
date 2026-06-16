import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NavController, LoadingController, ToastController } from '@ionic/angular';
import { Storage } from '@ionic/storage-angular';
import { JogoService, PLATAFORMAS, GENEROS } from '../../services/jogo.service';

@Component({
  selector: 'app-editar',
  templateUrl: 'editar.page.html',
  styleUrls: ['editar.page.scss'],
  standalone: false,
})
export class EditarPage implements OnInit {
  plataformas = PLATAFORMAS;
  generos = GENEROS;

  titulo = '';
  plataforma: number = 1;
  genero: number = 1;
  ano: number = new Date().getFullYear();
  desenvolvedor = '';

  private token = '';
  private jogoId = 0;

  constructor(
    private route: ActivatedRoute,
    private navCtrl: NavController,
    private loadingCtrl: LoadingController,
    private toastCtrl: ToastController,
    private storage: Storage,
    private jogoService: JogoService,
  ) {}

  async ngOnInit() {
    await this.storage.create();
    this.token = await this.storage.get('token');
    if (!this.token) { this.navCtrl.navigateRoot('/home'); return; }

    this.jogoId = Number(this.route.snapshot.paramMap.get('id'));

    const loading = await this.loadingCtrl.create({ message: 'Carregando...' });
    await loading.present();

    this.jogoService.buscar(this.token, this.jogoId).subscribe({
      next: async (jogo) => {
        this.titulo = jogo.titulo;
        this.plataforma = jogo.plataforma;
        this.genero = jogo.genero;
        this.ano = jogo.ano;
        this.desenvolvedor = jogo.desenvolvedor;
        await loading.dismiss();
      },
      error: async () => {
        await loading.dismiss();
        this.navCtrl.navigateRoot('/lista');
      }
    });
  }

  async salvar() {
    const loading = await this.loadingCtrl.create({ message: 'Salvando...' });
    await loading.present();

    const dados = {
      titulo: this.titulo,
      plataforma: this.plataforma,
      genero: this.genero,
      ano: this.ano,
      desenvolvedor: this.desenvolvedor,
    };

    this.jogoService.editar(this.token, this.jogoId, dados).subscribe({
      next: async () => {
        await loading.dismiss();
        const toast = await this.toastCtrl.create({
          message: 'Jogo atualizado com sucesso!',
          duration: 2000,
          color: 'success',
        });
        await toast.present();
        this.navCtrl.navigateRoot('/lista');
      },
      error: async () => {
        await loading.dismiss();
        const toast = await this.toastCtrl.create({
          message: 'Erro ao salvar o jogo.',
          duration: 2000,
          color: 'danger',
        });
        await toast.present();
      }
    });
  }

  cancelar() {
    this.navCtrl.navigateBack('/lista');
  }
}
