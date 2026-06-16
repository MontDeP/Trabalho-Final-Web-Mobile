from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('autenticacao-api/', views.LoginAPI.as_view(), name='autenticacao_api'),
    path('jogo/', include('jogo.urls')),
    path('avaliacao/', include('avaliacao.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
