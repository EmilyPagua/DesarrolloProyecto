from django.test import TestCase, RequestFactory    
from polls.RegistroFactory import *
from polls.views import *
from django.core.urlresolvers import reverse
from django.test.client import Client
from polls.models import UsuarioPerfil, Album ,Notificacion, Contenido, Historial, Contenido, Comentario, Like
from django.contrib.auth.models import User
import unittest


#1FORMS --------------Crear Usuario
class CrearUsuario(TestCase):    
    
    def setUp(self):                 
        self.data = {        
            'usuario': 'NombrePrueba',
            'clave': '12345678',
            'nombre': 'john',
            'apellido': 'ApellidoPrueba',
            'nacimiento': '02/01/1990',
            'direccion' : 'DireccionPrueba',
            'facebook' : 'Facebook Prueba',
            'correo' : 'prueba@prueba.com'
        }
        
    def test_NuevoUsuario(self):        
        Respuesta = RegistroUsuario(self.data)              
        if Respuesta.is_valid():
            resultado = Respuesta.procesar_registro()         
        
        usu = User.objects.count()    
        self.assertEquals(1,usu)     


#2FORMS --------------Modificar usuario
class ModificarUsuario(TestCase):        
    def setUp(self):                 
        self.client = Client()   
        self.usuario = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.usuarioperfil = Fac_UsuarioPerfil(fkusuario = self.usuario)                
        self.data = {        
            'clave': '12345678',
            'nombre': 'john',
            'apellido': 'ApellidoPrueba',
            'nacimiento': '02/01/1990',
            'direccion' : 'DireccionPrueba',
            'facebook' : 'Facebook Prueba',
            'correo' : 'prueba@prueba.com'
        }
        
    def test_EditarUsuario(self):                
        self.client.login(username=self.usuario.username, password='johnpassword')
        Respuesta = EditarUsuario(self.data)              
        if Respuesta.is_valid():
            resultado = Respuesta.modificar_registro(self.usuario)                 
        usu = User.objects.count()    
        self.assertEquals(1,usu)     


#3FORMS --------------Crear Album		
class CrearAlbum(TestCase):

    def setUp(self):        
        self.usuario = Fac_Usuario()        
        self.data = {
            'nombre': "Prueba",
            'descripcion': "Prueba album",
            'privacidad' : False          
   	    }
   	       	    
    def test_NuevoAlbum(self):
        albumes = Album.objects.count()  
        self.assertEquals(0,albumes)
        Respuesta = RegistroAlbum(self.data)
        if Respuesta.is_valid():
            resultado = Respuesta.procesar_album(self.usuario)         
        albumes = Album.objects.count()    
        self.assertEquals(1,albumes)


#4FORMS --------------Modificar Album		
class ModificarAlbum(TestCase):

    def setUp(self):                
        self.client = Client()   
        self.usuario = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')        
        self.album = Fac_Album(fkusuario = self.usuario)
        self.data = {
            'nombre': "Prueba 2",
            'descripcion': "Prueba album 2",
            'privacidad' : True          
   	    }
   	       	    
    def test_EditarAlbum(self):        
        Respuesta = RegistroAlbum(self.data)
        if Respuesta.is_valid():
            resultado = Respuesta.modificar_album(self.album)         
        albumes = Album.objects.count()    
        self.assertEquals(1,albumes)
             

#5FORMS --------------Registro Comentario	
class CrearComentario(TestCase):

    def setUp(self):                
        self.client = Client()   
        self.usuario = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')        
        self.album = Fac_Album(fkusuario = self.usuario)
        self.data = {
            'descripcion': "Es es un comentario nuevo",                   
   	    }
   	       	    
    def test_NuevoComentario(self):        
        Respuesta = RegistroComentario(self.data)
        if Respuesta.is_valid():
            resultado = Respuesta.procesar_comentario(self.album,self.usuario)
        comentar = Comentario.objects.count()    
        self.assertEquals(1,comentar)


#6VIEWS --------------Ver mis comentario
class VerMisComentarios(TestCase):

    def setUp(self): 
        self.client = Client()   
        self.usuario = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.usuarioperfil = Fac_UsuarioPerfil(fkusuario = self.usuario)                
   	       	    
    def test_VerMisComentarios(self):                
        self.client.login(username=self.usuario.username, password='johnpassword')
        response = self.client.get(reverse('comentar'))
        self.assertEqual(response.status_code, 200)
        
        
#7VIEWS --------------Principal Inicio (principal_inicio)
class PaginaPrincipal(TestCase):

    def setUp(self): 
        self.client = Client()   
        self.usuario = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')        
   	       	    
    def test_VerMisComentarios(self):                
        self.client.login(username=self.usuario.username, password='johnpassword')
        response = self.client.get(reverse('principalInicio'))
        self.assertEqual(response.status_code, 200)
        
   
#8VIEWS --------------Guardar Contenido (guardarFoto)----------------------
class GuardarContenido(TestCase):    
    def setUp(self): 
        
        self.client = Client()   
        self.usuario = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')        
        self.album = Fac_Album(fkusuario = self.usuario)        
        self.request = {
                      'imagenes[]': ['http://distilleryimage0.s3.amazonaws.com/10f276ee7fec11e3ad560e19b48852cc_6.jpg',
                                     'http://distilleryimage0.s3.amazonaws.com/10f276ee7fec11e3ad560e19b48852cc_7.jpg', 
                                     'http://api.soundcloud.com/tracks/87318020'],
                       'videos[]':  ['http://www.youtube.com/embed/X-77txuiVXs?autoplay=2&modestbranding=1', 
                                     'http://www.youtube.com/embed/X-77txuiVXs?autoplay=2&modestbranding=2']}        
           
    def test_GuardarfotoPost(self):                
        self.client.login(username=self.usuario.username, password='johnpassword')
        response = self.client.post(reverse('guardarFoto',kwargs={'id_album': self.album.id}),self.request)
        self.assertEqual(response.status_code, 200) 
   
    def test_GuardarfotoGet(self):                
        self.client.login(username=self.usuario.username, password='johnpassword')
        response = self.client.get(reverse('guardarFoto',kwargs={'id_album': self.album.id}),self.request)
        self.assertEqual(response.status_code, 404)          	    
 
 
 #9VIEWS --------------Guardar Contenido (agregarFoto)----------------------
class AgregarContenido(TestCase):    
    def setUp(self): 
        
        self.client = Client()   
        self.usuario = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')        
        self.album = Fac_Album(fkusuario = self.usuario)                      
        self.request = { 'hashtag': 'Playa'}   
           
    def test_AgregarContenidoPost(self):                
        self.client.login(username=self.usuario.username, password='johnpassword')
        response = self.client.post(reverse('agregarFoto',kwargs={'id_album': self.album.id}),self.request)
        self.assertEqual(response.status_code, 200) 
   
   
    def test_AgregarContenidoGet(self):                
        self.client.login(username=self.usuario.username, password='johnpassword')
        response = self.client.get(reverse('agregarFoto',kwargs={'id_album': self.album.id}),self.request)
        self.assertEqual(response.status_code, 200)   
               	    
 
 #10VIEWS --------------Guardar ReplicaComentario (replicarComentario)----------------------
class ReplicaComentario(TestCase):    
    def setUp(self): 
        
        self.client = Client()   
        self.usuario = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')        
        self.album = Fac_Album(fkusuario = self.usuario)   
        self.usuarioComentador = User.objects.create_user('ana', 'ana@thebeatles.com', 'anapassword')                
        self.comentario = Fac_Comentario(fkalbum = self.album, userComentador = self.usuarioComentador )                        
           
    def test_ReplicaComentarioPost(self):                
        self.client.login(username=self.usuario.username, password='johnpassword')
        response = self.client.post(reverse('replicarComentario',kwargs={'id_comentario': self.comentario.id}))
        self.assertEqual(response.status_code, 200) 
   
  
 #11VIEWS --------------VerNorificaciones (ver_notificacion)----------------------
class VerNorificaciones(TestCase):    
    def setUp(self):         
        self.client = Client()   
        self.usuario = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')                           
           
    def test_VerNorificacionesPost(self):                
        self.client.login(username=self.usuario.username, password='johnpassword')
        response = self.client.post(reverse('verNotificacion'))
        self.assertEqual(response.status_code, 200) 

    def test_VerNorificacionesGet(self):                
        self.client.login(username=self.usuario.username, password='johnpassword')
        response = self.client.get(reverse('verNotificacion'))
        self.assertEqual(response.status_code, 200)


#12VIEWS --------------RegistroAmistad (registro_amigo)----------------------
class RegistroAmistad(TestCase):    
    def setUp(self):         
        self.client = Client()   
        self.usuario = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')                           
        self.usuarioperfil = Fac_UsuarioPerfil(fkusuario = self.usuario)                
           
    def test_RegistroAmistadPost(self):                
        self.client.login(username=self.usuario.username, password='johnpassword')
        response = self.client.post(reverse('registroAmigo'))
        self.assertEqual(response.status_code, 200) 

    def test_VerNorificacionesGet(self):                
        self.client.login(username=self.usuario.username, password='johnpassword')
        response = self.client.post(reverse('registroAmigo'))
        self.assertEqual(response.status_code, 200)
        

#13VIEWS --------------BorrarAmigo (borrarAmigo)----------------------
class BorrarAmigo(TestCase):    
    def setUp(self):         
        self.client = Client()   
        self.usuario = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')                           
        self.usuarioperfil = Fac_UsuarioPerfil(fkusuario = self.usuario)                
        self.amigo = User.objects.create_user('ana', 'lennon@thebeatles.com', 'anapassword')                           
        self.amigoperfil = Fac_UsuarioPerfil2(fkusuario = self.amigo )                
           
    def test_BorrarAmigoGet(self):                
        self.client.login(username=self.usuario.username, password='johnpassword')
        response = self.client.get(reverse('borrarAmigo',kwargs={'id_amigo': self.amigo.id}))
        self.assertEqual(response.status_code, 200) 
  
  

#14VIEWS --------------Nolike (Nolike)----------------------
class Nolike(TestCase):    
    def setUp(self):         
        self.client = Client()   
        self.usuario = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')        
        self.album = Fac_Album(fkusuario = self.usuario)   
        self.usuarioComentador = User.objects.create_user('ana', 'ana@thebeatles.com', 'anapassword')                
        self.comentario = Fac_Comentario(fkalbum = self.album, userComentador = self.usuarioComentador )                        
        
           
    def test_NolikePost(self):                
        self.client.login(username=self.usuario.username, password='johnpassword')
        response = self.client.post(reverse('Nolike',kwargs={'id_comentario': self.comentario.id}))
        self.assertEqual(response.status_code, 200) 

#15VIEWS --------------likeComentario (likeComentario)----------------------
class like(TestCase):    
    def setUp(self):         
        self.client = Client()   
        self.usuario = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')        
        self.album = Fac_Album(fkusuario = self.usuario)   
        self.usuarioComentador = User.objects.create_user('ana', 'ana@thebeatles.com', 'anapassword')                
        self.comentario = Fac_Comentario(fkalbum = self.album, userComentador = self.usuarioComentador )                        
        
           
    def test_NolikePost(self):                
        self.client.login(username=self.usuario.username, password='johnpassword')
        response = self.client.post(reverse('likeComentario',kwargs={'id_comentario': self.comentario.id}))
        self.assertEqual(response.status_code, 200) 

detalle_album
#16VIEWS --------------EscribirReplicaComentario (EscribirReplicaComentario)----------------------
class EscribirReplicaComentario(TestCase):    
    def setUp(self):         
        self.client = Client()   
        self.usuario = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')        
        self.album = Fac_Album(fkusuario = self.usuario)   
        self.usuarioComentador = User.objects.create_user('ana', 'ana@thebeatles.com', 'anapassword')                
        self.comentario = Fac_Comentario(fkalbum = self.album, userComentador = self.usuarioComentador )                        
        
           
    def test_EscribirReplicaComentarioPost(self):                
        self.client.login(username=self.usuario.username, password='johnpassword')
        response = self.client.post(reverse('EscribirReplicaComentario',kwargs={'id_comentario': self.comentario.id}))
        self.assertEqual(response.status_code, 200) 


#17VIEWS --------------DetalleAlbum (DetalleAlbum)----------------------
class DetalleAlbum(TestCase):    
    def setUp(self):         
        self.client = Client()   
        self.usuario = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')        
        self.album = Fac_Album(fkusuario = self.usuario)   
        
           
    def test_EscribirReplicaComentarioPost(self):                
        self.client.login(username=self.usuario.username, password='johnpassword')
        response = self.client.post(reverse('detalleAlbum',kwargs={'id_album': self.album.id}))
        self.assertEqual(response.status_code, 200) 
                
