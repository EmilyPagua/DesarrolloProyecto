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
	twitter = models.CharField(max_length=50)
	facebook = models.CharField(max_length=50)
	privacidad = models.BooleanField(max_length=50)
	foto = models.ImageField(upload_to='imagenusuario', null=True,blank=True)

	def __str__(self):
		return self.fkusuario.username

class RelacionUsuario(models.Model):
    fkamigo = models.ForeignKey(User) #es el que NO esta logueado
    usuario = models.ForeignKey(UsuarioPerfil) # es el usuario Logueado
    
    class Meta:
        unique_together = ['fkamigo', 'usuario']

	def __str__(self):
		return '%s %s' % (self.fkamigo, self.usuario)

class Calendario(models.Model):
	fecha = models.DateTimeField('date published')

	def __str__(self):
		return '%s' % self.fecha


class Instagram(models.Model):
	url = models.CharField(max_length=200)

	def __str__(self):
		return self.url


class SoundCloud(models.Model):
	url = models.CharField(max_length=200)

	def __str__(self):
		return self.url


class YouTube(models.Model):
	url = models.CharField(max_length=200)

	def __str__(self):
		return self.url


class Album(models.Model):
	nombre = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=200)
	privacidad = models.BooleanField(default=True)
	foto = models.ImageField(upload_to='imagenalbum')
	fkusuario = models.ForeignKey(User)
	fkcalendario = models.ForeignKey(Calendario)

	def __str__(self):
		return self.nombre


class Comentario(models.Model):
	descripcion	= models.CharField(max_length=200)
	fkemisor = models.ForeignKey(User)
	fkalbum	= models.ForeignKey(Album)
	fkinstagram	= models.ForeignKey(Instagram)
	fkyoutube = models.ForeignKey(YouTube)
	fksoundcloud = models.ForeignKey(SoundCloud)
	fkcalendario = models.ForeignKey(Calendario)
	
	def __str__(self):
		return self.descripcion


class MeGusta(models.Model):
	like = models.CharField(max_length=200)
	fkemisor = models.ForeignKey(User)
	fkalbum	= models.ForeignKey(Album)
	fkinstagram	= models.ForeignKey(Instagram)
	fkyoutube = models.ForeignKey(YouTube)
	fksoundcloud = models.ForeignKey(SoundCloud)
	fkcalendario = models.ForeignKey(Calendario)

	def __str__(self):
		return self.like

class Notificacion(models.Model):
	fkemisor = models.ForeignKey(User)
	fkalbum	= models.ForeignKey(Album)
	fkinstagram	= models.ForeignKey(Instagram)
	fkyoutube = models.ForeignKey(YouTube)
	fksoundcloud = models.ForeignKey(SoundCloud)
	fkcalendario = models.ForeignKey(Calendario)
	

class RelacionNotificacion(models.Model):
	fknotificacion = models.ManyToManyField(Notificacion)


class RelacionComentario(models.Model):
	fkcomentario = models.ManyToManyField(Comentario)

