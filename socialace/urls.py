#coding=utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', login,{'template_name':'login_principal.html'}, name='loginPrincipal'),
    url(r'^loginPrincipal/$', login,{'template_name':'login_principal.html'}, name='login'),
    url(r'^principalInicio/$', 'polls.views.principal_inicio', name='principalInicio'),
    url(r'^logout/$', logout, {'next_page': '/loginPrincipal/'} ,name='logout'),
    
    url(r'^registroUsuario/$', 'polls.views.registro_usuario', name='registroUsuario'),
    url(r'^modificarUsuario/(?P<id_usuario>\d+)/$', 'polls.views.modificar_usuario',name ='modificarUsuario'),
    url(r'^MiPerfil/(?P<id_usuario>\d+)/$', 'polls.views.ver_MiPerfil',name ='Miperfil'),    
    
    url(r'^registroAlbum/$', 'polls.views.registro_album',name ='registroAlbum'),
    url(r'^modificarAlbum/(?P<id_album>\d+)/$', 'polls.views.modificar_album',name ='modificarAlbum'),
    url(r'^verAlbumes/$', 'polls.views.ver_albumes',name ='verAlbumes'),    
    url(r'^agregarFoto/(?P<id_album>\d+)/$', 'polls.views.registro_foto',name ='agregarFoto'),
    url(r'^detalleAlbum/(?P<id_album>\d+)/$', 'polls.views.detalle_album', name='detalleAlbum'), 

    url(r'^detalleAlbum2/(?P<id_album>\d+)/$', 'polls.views.detalle_album2', name='detalleAlbum2'), 
    url(r'^registroAmigo/$', 'polls.views.registro_amigo',name ='registroAmigo'),
    url(r'^verAmigos/$', 'polls.views.ver_amigos',name ='verAmigos'),
    url(r'^verUsuario/(?P<nombre>.+)/$', 'polls.views.ver_usuario',name ='verUsuario'),
    url(r'^buscar/$', 'polls.views.busqueda',name ='busqueda'),
    url(r'^perfilAmigo/(?P<id_usuario>\d+)/$', 'polls.views.ver_PerfilAmigo',name ='perfilAmigo'),    
    
    url(r'^verNotificacion/$', 'polls.views.ver_notificacion',name ='verNotificacion'),    
    url(r'^notificacioneAprobadas/(?P<id_notificacion>\d+)/$', 'polls.views.notificaciones_aprobadas',name ='notificacionesAprobadas'),
    url(r'^MisNotificaciones/$', 'polls.views.notificaciones_aceptadas',name ='misNotificaciones'),
    
    
    url(r'', include('social_auth.urls')),    
    url(r'^prueba/(?P<id_album>\d+)/$', 'polls.views.prueba', name='prueba'),    
)
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
