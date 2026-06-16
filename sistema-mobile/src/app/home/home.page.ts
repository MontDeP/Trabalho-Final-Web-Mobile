import { Component, OnInit } from '@angular/core';
import { LoadingController, NavController, AlertController, ToastController } from '@ionic/angular';
import { Storage } from '@ionic/storage-angular';
import { AutenticacaoService } from '../services/autenticacao.service';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  standalone: false,
})
export class HomePage implements OnInit {
  username: string = '';
  password: string = '';

  constructor(
    private loadingCtrl: LoadingController,
    private navCtrl: NavController,
    private alertCtrl: AlertController,
    private toastCtrl: ToastController,
    private storage: Storage,
    private autenticacaoService: AutenticacaoService,
  ) {}

  async ngOnInit() {
    await this.storage.create();
    const token = await this.storage.get('token');
    if (token) {
      this.navCtrl.navigateRoot('/lista');
    }
  }

  async autenticarUsuario() {
    const loading = await this.loadingCtrl.create({ message: 'Autenticando...' });
    await loading.present();

    this.autenticacaoService.login(this.username, this.password).subscribe({
      next: async (resposta) => {
        await loading.dismiss();
        await this.storage.set('token', resposta.token);
        await this.storage.set('usuario', resposta);
        this.navCtrl.navigateRoot('/lista');
      },
      error: async () => {
        await loading.dismiss();
        const alert = await this.alertCtrl.create({
          header: 'Erro de Login',
          message: 'Usuário ou senha inválidos.',
          buttons: ['OK']
        });
        await alert.present();
      }
    });
  }
}
