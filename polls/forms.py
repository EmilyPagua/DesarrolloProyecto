# -*- encoding: utf-8 -*-
from django import forms
from polls.models import UsuarioPerfil,  Album, Notificacion,Historial, Contenido,Comentario
from django.contrib.auth.models import User
import datetime


class RegistroUsuario(forms.Form):
    usuario = forms.CharField(max_length=50, label='Usuario (*)')
    clave =  forms.CharField(max_length=20, widget=forms.PasswordInput,label='Clave (*)')
    nombre =  forms.CharField(max_length=50, label='Nombre (*)')
    apellido = forms.CharField(max_length=50, label='Apellido (*)')
    nacimiento = forms.CharField(max_length=50, label='Nacimiento (*)')
    direccion =  forms.CharField(max_length=50, label='Direccion (*)')
    facebook =  forms.CharField(max_length=50, label='Facebook',required=False)
    correo =  forms.CharField(max_length=50, label='Correo')    
    foto = forms.ImageField(label='Foto', required=False)    
    privacidad =  forms.BooleanField(label='Privacidad',required=False)
    
    def __init__(self, *args, **kwargs):
        super(RegistroUsuario, self).__init__(*args, **kwargs)
        self.fields['usuario'].widget.attrs = {'placeholder': 'usuario', 'class': 'form-control','name':'usuario'}
        self.fields['clave'].widget.attrs = {'placeholder': 'clave', 'class': 'form-control'}
        self.fields['nombre'].widget.attrs = {'placeholder': 'nombre', 'class': 'form-control'}
        self.fields['apellido'].widget.attrs = {'placeholder': 'apellido', 'class': 'form-control'}
        self.fields['nacimiento'].widget.attrs = {'placeholder': 'nacimiento', 'class': 'datepicker form-control'}
        self.fields['direccion'].widget.attrs = {'placeholder': 'direccion', 'class': 'form-control'}
        self.fields['facebook'].widget.attrs = {'placeholder': 'facebook', 'class': 'form-control'}
        self.fields['correo'].widget.attrs = {'placeholder': 'correo', 'class': 'form-control'}
        self.fields['foto'].widget.attrs = {'placeholder': 'foto', 'class': 'form-control'}
   
    def clean_nacimiento(self):
        fecha = self.cleaned_data['nacimiento'].split('/')
        fecha = map(int, fecha)
        fecha = datetime.date(year=fecha[2], month=fecha[1], day=fecha[0])
        hoy = datetime.date.today()
        if fecha >= hoy:
            raise forms.ValidationError("Fecha de nacimiento, no puede ser mayor o igual a la de hoy")
        return fecha
   
    def procesar_registro(self):
        username = self.cleaned_data['usuario']
        password = self.cleaned_data['clave']
        name = self.cleaned_data['nombre']
        lastname = self.cleaned_data['apellido']
        fechaNac = self.cleaned_data['nacimiento']
        direccion = self.cleaned_data['direccion']
        facebook = self.cleaned_data['facebook']
        email = self.cleaned_data['correo']
        privacidad = self.cleaned_data['privacidad']
        foto = self.cleaned_data.get('foto')
        usuario = User(username=username, first_name=name, last_name=lastname, email=email)
        usuario.set_password(password)
        usuario.save()
        perfil = UsuarioPerfil(fechanacimiento=fechaNac, direccion=direccion,  facebook=facebook, privacidad=privacidad, fkusuario=usuario)
        if foto:
            perfil.foto = foto
        perfil.save()

        
class EditarUsuario(forms.Form):    
    clave =  forms.CharField(max_length=20, widget=forms.PasswordInput,label='Clave (*)')
    nombre =  forms.CharField(max_length=50, label='Nombre (*)')
    apellido = forms.CharField(max_length=50, label='Apellido (*)')
    nacimiento = forms.CharField(max_length=50, label='Nacimiento (*)')
    direccion =  forms.CharField(max_length=50, label='Direccion (*)')
    facebook =  forms.CharField(max_length=50, label='Facebook',required=False)    
    correo =  forms.CharField(max_length=50, label='Correo')
    privacidad =  forms.BooleanField(label='Privacidad',required=False)
    foto = forms.ImageField(label='Foto', required=False)    
    
  
    def __init__(self, *args, **kwargs):
        super(EditarUsuario, self).__init__(*args, **kwargs)
        self.fields['clave'].widget.attrs = {'placeholder': 'clave', 'class': 'form-control'}
        self.fields['nombre'].widget.attrs = {'placeholder': 'nombre', 'class': 'form-control'}
        self.fields['apellido'].widget.attrs = {'placeholder': 'apellido', 'class': 'form-control'}
        self.fields['nacimiento'].widget.attrs = {'placeholder': 'nacimiento', 'class': 'datepicker form-control'}
        self.fields['direccion'].widget.attrs = {'placeholder': 'direccion', 'class': 'form-control'}
        self.fields['facebook'].widget.attrs = {'placeholder': 'facebook', 'class': 'form-control'}
        self.fields['foto'].widget.attrs = {'placeholder': 'foto', 'class': 'form-control'}
        self.fields['correo'].widget.attrs = {'placeholder': 'correo', 'class': 'form-control'}
        
    def clean_nacimiento(self):
        fecha = self.cleaned_data['nacimiento'].split('/')
        fecha = map(int, fecha)
        fecha = datetime.date(year=fecha[2], month=fecha[1], day=fecha[0])
        hoy = datetime.date.today()
        if fecha >= hoy:
            raise forms.ValidationError("Fecha de nacimiento, no puede ser mayor o igual a la de hoy")
        return fecha
        
    def modificar_registro(self, usuario):
        (self.cleaned_data['clave'])        
        print "en el modificar_registro"
        usuario.first_name = self.cleaned_data['nombre']
        usuario.last_name = self.cleaned_data['apellido']
        usuario.usuarioperfil.fechanacimiento = self.cleaned_data['nacimiento']
        usuario.usuarioperfil.direccion = self.cleaned_data['direccion']        
        usuario.usuarioperfil.facebook = self.cleaned_data['facebook']
        usuario.email = self.cleaned_data['correo']
        usuario.usuarioperfil.privacidad = self.cleaned_data['privacidad']
        #foto = self.cleaned_data.get('foto', None)
        foto = self.cleaned_data['foto']   
        print foto
        if foto:
            usuario.usuarioperfil.foto = foto
        usuario.usuarioperfil.save()
        usuario.save()


#Formulario del Album
class RegistroAlbum(forms.Form):
    nombre = forms.CharField(max_length=50, label='Nombre (*)')
    descripcion = forms.CharField(widget=forms.Textarea,label='Descripcion (*)',max_length=1000)
    privacidad = forms.BooleanField(label='Privacidad',required=False)
    foto = forms.ImageField(label='Foto', required=False)   
   
    def __init__(self,*args, **kwargs):
        super(RegistroAlbum, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs = {'placeholder': 'nombre', 'class': 'form-control'}
        self.fields['descripcion'].widget.attrs = {'placeholder': 'descripcion'}
        self.fields['foto'].widget.attrs = {'placeholder': 'foto', 'class': 'form-control'}
        
    def procesar_album(self,usuario):
        nombre = self.cleaned_data['nombre']
        descripcion = self.cleaned_data['descripcion']
        privacidad = self.cleaned_data['privacidad']
        foto = self.cleaned_data['foto']        
        album = Album(nombre=nombre, descripcion=descripcion, privacidad=privacidad, fkusuario=usuario)        
        if foto:
            album.foto = foto
        album.save()   
             
        b = Historial(usuario=usuario, accion='Nuevo album',fkalbum=album)
        b.save()

    def modificar_album(self, album):
        album.nombre = self.cleaned_data['nombre']
        album.descripcion = self.cleaned_data['descripcion']
        album.privacidad = self.cleaned_data['privacidad']
        foto = self.cleaned_data['foto']      
        if foto:
            album.foto = foto
        album.save()    


#Relacion Usuario
class RegistroAmigo(forms.Form):
    amigos = forms.CharField(label='Amigos') 
    
    def __init__(self,*args, **kwargs):	
        super(RegistroAmigo, self).__init__(*args, **kwargs)
        self.fields['amigos'].widget.attrs = {'placeholder': 'amigos', 'class': 'admin-form'}#,'style':'visibility:hidden'}
        
    def procesar_notificacion(self, usuario):      	
        id_amigo = self.cleaned_data['amigos']
        #import pdb; pdb.set_trace()   
        print self.cleaned_data['amigos']    
        l = User.objects.get(username=id_amigo)
        k = User.objects.get(id=usuario.id)
        print l
        #llenar historial
        b = Historial(usuario=k, accion='Amistad')
        b.save()
        #llenar notificacion
        c = Notificacion(usuario=l, historia=b, descripcion ='Amistad')
        c.save()
       

#ACOMODANDO
    def procesar_amigo(self, usuario):        
        k = User.objects.get(id=usuario.id)
        id_amigo = self.cleaned_data['amigos']                   
        l = User.objects.get(username=id_amigo)
        
       

#Formulario del Comentario
class RegistroComentario(forms.Form):
    descripcion = forms.CharField(widget=forms.Textarea,label='Comentario (*)',max_length=1000)   
   
    def __init__(self,*args, **kwargs):
        super(RegistroComentario, self).__init__(*args, **kwargs)
        self.fields['descripcion'].widget.attrs = {'placeholder': 'descripcion', 'class': 'form-control'}
        
    def procesar_comentario(self,albumes,usuario):        
        descripcio = self.cleaned_data['descripcion']        
        count = Comentario.objects.filter(fkalbum=albumes, descripcion=descripcio, userComentador=usuario)
        if count:
    	    for aux in count: 
                aux.delete() 
        comentar = Comentario(fkalbum=albumes, descripcion=descripcio, userComentador=usuario)        
        comentar.save()        
        l = Comentario.objects.get(fkalbum=albumes, descripcion=descripcio, userComentador=usuario)
        k = User.objects.get(id=albumes.fkusuario.id)
        b = Historial(usuario=k, accion='comentario',fkcomentario=l)
        b.save()
     
    def procesar_replica(self,albumes,usuario,comentReplic):        
        descripcio = self.cleaned_data['descripcion']        
        count = Comentario.objects.filter(fkalbum=albumes, descripcion=descripcio, userComentador=usuario,replica=comentReplic)
        print albumes.id
        print usuario.username
        if count:
    	    for aux in count: 
                aux.delete()    	
    
        comentar = Comentario(fkalbum=albumes, descripcion=descripcio, userComentador=usuario,replica=comentReplic)        
        comentar.save()        
        l = Comentario.objects.get(fkalbum=albumes, descripcion=descripcio, userComentador=usuario,replica=comentReplic)
        k = User.objects.get(id=albumes.fkusuario.id)
        b = Historial(usuario=k, accion='comentario',fkcomentario=l)
        b.save()
        
        

#buscandoHashtag
class BuscarHashtag(forms.Form):
   hashtag = forms.CharField(max_length=50, label='Introduzca un hashtag')      
 
   def __init__(self,*args, **kwargs):
       super(BuscarHashtag, self).__init__(*args, **kwargs)
       self.fields['hashtag'].widget.attrs = {'placeholder': 'hashtag', 'class': 'form-control'}        
       
   def procesar_album(self,usuario):
       hashtag = self.cleaned_data['hashtag']

