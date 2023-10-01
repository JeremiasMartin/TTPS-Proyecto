from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('registro_representante/', views.representante_signup, name='registro_representante'),
    path('perfil_representante/', views.perfil_representante, name='perfil_representante'),
    path('editar_perfil_representante/', views.editar_perfil_representante, name='editar_perfil_representante'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('restablecer_contrasenia/', views.restablecer_contraseña, name='Restablecer_contrasenia'),
    path('restablecer_contrasenia_enviado/', views.restDone, name='restablecer_contrasenia_enviado'),
    path('reset/<uidb64>/<token>', views.restPasswordConfirm.as_view(template_name='usuario/cambio_de_clave/rest-contra-conf.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="usuario/cambio_de_clave/restablecer_contrasenia_exitoso.html"), name='password_reset_complete'),
    path('cambiar_contrasenia/', views.cambiar_contrasenia.as_view(template_name='usuario/cambio_de_clave/cambiar_contrasenia.html')),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
