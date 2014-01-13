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
        

#7VIEWS --------------Guardar Contenido (guardarFoto)
class AgregarContenido(TestCase):
    def setUp(self): 
        self.client = Client()   
        self.usuario = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.album = Fac_Album(fkusuario = self.usuario)
        self.imagenes = {'http://distilleryimage5.s3.amazonaws.com/aed48bf45ec211e38bd512a12d5e0079_6.jpg', 
                       'http://distilleryimage7.s3.amazonaws.com/ba60d4bc5ebf11e38ec60ed5b89ef40f_6.jpg',}
   	       	    
    def test_GuardarContenido(self):                
        self.client.login(username=self.usuario.username, password='johnpassword')
        response = self.client.get(reverse('guardarFoto', self.album))
        self.assertEqual(response.status_code, 200)        
        
