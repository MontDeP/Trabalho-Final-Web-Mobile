import { Component, OnInit } from '@angular/core';
import { NavController } from '@ionic/angular';
import { Storage } from '@ionic/storage-angular';
import { AvaliacaoService, Avaliacao } from '../../services/avaliacao.service';

@Component({
  selector: 'app-avaliacoes',
  templateUrl: 'avaliacoes.page.html',
  styleUrls: ['avaliacoes.page.scss'],
  standalone: false,
})
export class AvaliacoesPage implements OnInit {
  itens: Avaliacao[] = [];
  carregando = true;
  usuarioId: number | null = null;
  mostrarMinhas = false;

  get itensFiltrados(): Avaliacao[] {
    if (this.mostrarMinhas) {
      return this.itens.filter(av => av.usuario === this.usuarioId);
    }
    return this.itens;
  }

  constructor(
    private storage: Storage,
    private avaliacaoService: AvaliacaoService,
    private navCtrl: NavController,
  ) {}

  async ngOnInit() {
    await this.storage.create();
    const token = await this.storage.get('token');
    if (!token) { this.navCtrl.navigateRoot('/home'); return; }

    const usuario = await this.storage.get('usuario');
    if (usuario) { this.usuarioId = usuario.id; }

    this.avaliacaoService.listar(token).subscribe({
      next: (dados) => { this.itens = dados; this.carregando = false; },
      error: () => { this.carregando = false; }
    });
  }

  voltar() {
    this.navCtrl.navigateBack('/lista');
  }

  toggleMinhas() {
    this.mostrarMinhas = !this.mostrarMinhas;
  }

  novaAvaliacao() {
    this.navCtrl.navigateForward('/nova-avaliacao');
  }

  editarAvaliacao(id: number) {
    this.navCtrl.navigateForward(`/editar-avaliacao/${id}`);
  }

  estrelas(nota: number): string {
    const cheia = Math.floor(nota);
    return '★'.repeat(cheia) + '☆'.repeat(10 - cheia);
  }

  formatarData(dataStr: string): string {
    return new Date(dataStr).toLocaleDateString('pt-BR');
  }
}
