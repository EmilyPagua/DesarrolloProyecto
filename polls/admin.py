from django.contrib import admin
from polls.models import UsuarioPerfil, Calendario, Instagram, SoundCloud, YouTube, Album, Comentario, MeGusta, RelacionComentario, RelacionNotificacion, Notificacion

admin.site.register(UsuarioPerfil)
admin.site.register(Calendario)
admin.site.register(Instagram)
admin.site.register(SoundCloud)
admin.site.register(YouTube)
admin.site.register(Album)
admin.site.register(Comentario)
admin.site.register(MeGusta)
admin.site.register(Notificacion)
admin.site.register(RelacionNotificacion)
admin.site.register(RelacionComentario)

