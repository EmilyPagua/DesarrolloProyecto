#encoding:utf-8
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import datetime


# Create your models here.
class UsuarioPerfil(models.Model):
	fkusuario = models.OneToOneField(User)
	fechanacimiento	= models.DateField(max_length=50)
	direccion = models.CharField(max_length=100)
	facebook = models.CharField(max_length=50)
	privacidad = models.BooleanField( default=False)
	foto = models.ImageField(upload_to='imagenusuario', null=True,blank=True)
	amigos = models.ManyToManyField(User, related_name ='amigos', null=True,blank=True)

	def __str__(self):
		datos = self.fkusuario.username+ ', '+ self.fkusuario.last_name+' - ' +self.fkusuario.first_name
		return datos
	
	class Meta: 
		ordering = ('fkusuario',)


class Album(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.TextField(verbose_name='Descripcion',max_length=1000)
	privacidad = models.BooleanField(default=False)
	foto = models.ImageField(upload_to='imagenalbum', null=True,blank=True)
	fkusuario = models.ForeignKey(User)

	def __str__(self):
		return self.nombre


class Contenido(models.Model):
    fkalbum	= models.ForeignKey(Album)
    urlfoto = models.CharField(max_length=200,null=True,blank=True)
    urlvideo = models.CharField(max_length=200,null=True,blank=True)
    urlaudio = models.CharField(max_length=200,null=True,blank=True)
	
    def __str__(self):
        return self.fkalbum.nombre

class Comentario(models.Model):
    fkalbum	= models.ForeignKey(Album)
    userComentador = models.ForeignKey(User)
    descripcion	= models.TextField(verbose_name='Descripcion',max_length=1000)
    replica = models.ForeignKey('self', null=True,blank=True)
	
    def __str__(self):
        return self.descripcion +' '+self.userComentador.username


class Like(models.Model):
    userLike = models.ForeignKey(User)
    fkalbum	= models.ForeignKey(Album, null=True,blank=True)
    fkcomentario = models.ForeignKey(Comentario, null=True,blank=True)
    like = models.BooleanField(default=False)
    
    def __str__(self):
		datos = self.userLike.username+ ', '+ self.userLike.last_name+' - ' +self.userLike.first_name
		return datos

class Historial(models.Model):
	usuario = models.ForeignKey(User)
	accion = models.CharField(max_length=200)
	fkalbum	= models.ForeignKey(Album,null=True,blank=True)
	fkcomentario = models.ForeignKey(Comentario, null=True,blank=True)
	fklike = models.ForeignKey(Like, null=True, blank=True)
	
	def __str__(self):
		return self.usuario.username+' '+self.accion

	
class Notificacion(models.Model):
	usuario = models.ForeignKey(User)
	historia = models.ForeignKey(Historial, null=True,blank=True)
	descripcion = models.CharField(max_length=200)
	status = models.BooleanField( default=False)	
	
	def __str__(self):
		return self.usuario.username + '  <---  '+ self.historia.usuario.username 

