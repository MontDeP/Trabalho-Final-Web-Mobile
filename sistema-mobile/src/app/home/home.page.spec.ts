import { ComponentFixture, TestBed, fakeAsync, flushMicrotasks } from '@angular/core/testing';
import { NavController, LoadingController, AlertController, ToastController, IonicModule } from '@ionic/angular';
import { of, throwError } from 'rxjs';

import { HomePage } from './home.page';
import { AutenticacaoService } from '../services/autenticacao.service';
import { Storage } from '@ionic/storage-angular';

const storageMock = {
  create: jasmine.createSpy('create').and.returnValue(Promise.resolve()),
  get: jasmine.createSpy('get').and.returnValue(Promise.resolve(null)),
  set: jasmine.createSpy('set').and.returnValue(Promise.resolve()),
};

const navCtrlMock = {
  navigateRoot: jasmine.createSpy('navigateRoot'),
  navigateForward: jasmine.createSpy('navigateForward'),
};

const loadingMock = {
  present: jasmine.createSpy('present').and.returnValue(Promise.resolve()),
  dismiss: jasmine.createSpy('dismiss').and.returnValue(Promise.resolve()),
};

const loadingCtrlMock = {
  create: jasmine.createSpy('create').and.returnValue(Promise.resolve(loadingMock)),
};

const alertMock = {
  present: jasmine.createSpy('present').and.returnValue(Promise.resolve()),
};

const alertCtrlMock = {
  create: jasmine.createSpy('create').and.returnValue(Promise.resolve(alertMock)),
};

const toastCtrlMock = {
  create: jasmine.createSpy('create').and.returnValue(Promise.resolve({ present: () => Promise.resolve() })),
};

const autenticacaoServiceMock = {
  login: jasmine.createSpy('login'),
};

describe('HomePage', () => {
  let component: HomePage;
  let fixture: ComponentFixture<HomePage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HomePage],
      imports: [IonicModule.forRoot()],
      providers: [
        { provide: Storage, useValue: storageMock },
        { provide: NavController, useValue: navCtrlMock },
        { provide: LoadingController, useValue: loadingCtrlMock },
        { provide: AlertController, useValue: alertCtrlMock },
        { provide: ToastController, useValue: toastCtrlMock },
        { provide: AutenticacaoService, useValue: autenticacaoServiceMock },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(HomePage);
    component = fixture.componentInstance;
  });

  it('deve criar o componente', () => {
    expect(component).toBeTruthy();
  });

  it('deve redirecionar para /lista se já houver token salvo', async () => {
    storageMock.get.and.returnValue(Promise.resolve('token-existente'));
    await component.ngOnInit();
    expect(navCtrlMock.navigateRoot).toHaveBeenCalledWith('/lista');
  });

  it('não deve redirecionar se não houver token', async () => {
    storageMock.get.and.returnValue(Promise.resolve(null));
    navCtrlMock.navigateRoot.calls.reset();
    await component.ngOnInit();
    expect(navCtrlMock.navigateRoot).not.toHaveBeenCalled();
  });

  it('deve salvar token e navegar para /lista após login com sucesso', fakeAsync(() => {
    const respostaLogin = { id: 1, nome: 'Admin', email: 'a@a.com', token: 'abc123' };
    autenticacaoServiceMock.login.and.returnValue(of(respostaLogin));
    storageMock.set.calls.reset();
    navCtrlMock.navigateRoot.calls.reset();

    component.username = 'admin';
    component.password = '1234';
    component.autenticarUsuario();
    flushMicrotasks();

    expect(storageMock.set).toHaveBeenCalledWith('token', 'abc123');
    expect(navCtrlMock.navigateRoot).toHaveBeenCalledWith('/lista');
  }));

  it('deve exibir alerta de erro quando login falhar', fakeAsync(() => {
    autenticacaoServiceMock.login.and.returnValue(throwError(() => new Error('401')));
    alertCtrlMock.create.calls.reset();
    alertMock.present.calls.reset();

    component.username = 'errado';
    component.password = 'errado';
    component.autenticarUsuario();
    flushMicrotasks();

    expect(alertCtrlMock.create).toHaveBeenCalled();
    expect(alertMock.present).toHaveBeenCalled();
  }));
});
