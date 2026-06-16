import { Component, OnInit } from '@angular/core';
import { NavController, LoadingController, ToastController } from '@ionic/angular';
import { Storage } from '@ionic/storage-angular';
import { JogoService, PLATAFORMAS, GENEROS } from '../../services/jogo.service';

@Component({
  selector: 'app-novo',
  templateUrl: 'novo.page.html',
  styleUrls: ['novo.page.scss'],
  standalone: false,
})
export class NovoPage implements OnInit {
  plataformas = PLATAFORMAS;
  generos = GENEROS;

  titulo = '';
  plataforma: number = 1;
  genero: number = 1;
  ano: number = new Date().getFullYear();
  desenvolvedor = '';
  fotoArquivo: File | null = null;
  fotoPreview: string | null = null;

  private token = '';

  constructor(
    private navCtrl: NavController,
    private loadingCtrl: LoadingController,
    private toastCtrl: ToastController,
    private storage: Storage,
    private jogoService: JogoService,
  ) {}

  async ngOnInit() {
    await this.storage.create();
    this.token = await this.storage.get('token');
    if (!this.token) { this.navCtrl.navigateRoot('/home'); }
  }

  selecionarFoto(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      this.fotoArquivo = input.files[0];
      const reader = new FileReader();
      reader.onload = (e) => { this.fotoPreview = e.target?.result as string; };
      reader.readAsDataURL(this.fotoArquivo);
    }
  }

  removerFoto() {
    this.fotoArquivo = null;
    this.fotoPreview = null;
  }

  async salvar() {
    if (!this.titulo.trim() || !this.desenvolvedor.trim()) {
      const toast = await this.toastCtrl.create({
        message: 'Preencha todos os campos obrigatórios.',
        duration: 2000,
        color: 'warning',
      });
      await toast.present();
      return;
    }

    const loading = await this.loadingCtrl.create({ message: 'Salvando...' });
    await loading.present();

    let dados: FormData | object;
    if (this.fotoArquivo) {
      const fd = new FormData();
      fd.append('titulo', this.titulo);
      fd.append('plataforma', String(this.plataforma));
      fd.append('genero', String(this.genero));
      fd.append('ano', String(this.ano));
      fd.append('desenvolvedor', this.desenvolvedor);
      fd.append('foto', this.fotoArquivo, this.fotoArquivo.name);
      dados = fd;
    } else {
      dados = {
        titulo: this.titulo,
        plataforma: this.plataforma,
        genero: this.genero,
        ano: this.ano,
        desenvolvedor: this.desenvolvedor,
      };
    }

    this.jogoService.criar(this.token, dados).subscribe({
      next: async () => {
        await loading.dismiss();
        const toast = await this.toastCtrl.create({
          message: 'Jogo cadastrado com sucesso!',
          duration: 2000,
          color: 'success',
        });
        await toast.present();
        this.navCtrl.navigateRoot('/lista');
      },
      error: async () => {
        await loading.dismiss();
        const toast = await this.toastCtrl.create({
          message: 'Erro ao cadastrar o jogo.',
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
