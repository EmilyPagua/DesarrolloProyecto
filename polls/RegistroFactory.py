from polls.models import UsuarioPerfil, Album ,Notificacion, Contenido, Historial, Contenido, Comentario, Like
from django.contrib.auth.models import User
import factory

#Usuario
class Fac_Usuario(factory.Factory):
    FACTORY_FOR = User
    
    username = factory.Sequence(lambda x: 'usuario%s' % x)
    first_name = "Mimia"
    last_name = "Lo"    
    email = "mimiaLo@gmail.com"
    
    @classmethod
    def _prepare(cls, create, **kwargs):
        p=super(cls,Fac_Usuario)._prepare(create, **kwargs)
        p.set_password('12345678')
        if create:
            p.save()
        return p

#Perfil Usuario
class Fac_UsuarioPerfil(factory.Factory):
    FACTORY_FOR = UsuarioPerfil
    fechanacimiento	= '1991-02-01'
    direccion = 'Caracas'
    facebook = 'PruebaCaracas'
    privacidad = False
    
    @classmethod
    def _prepare(cls, create, **kwargs):
        p=super(cls,Fac_UsuarioPerfil)._prepare(create, **kwargs)
        if create:
            p.save()
        return p   
 
#Album
class Fac_Album(factory.Factory):
    FACTORY_FOR = Album
    nombre = 'Album 1'
    descripcion = 'Album prueba 1'
    privacidad = False 
    
    @classmethod
    def _prepare(cls, create, **kwargs):
        p=super(cls,Fac_Album)._prepare(create, **kwargs)
        if create:
            p.save()
        return p   


