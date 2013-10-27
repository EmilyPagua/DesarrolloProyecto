from django import forms
from polls.models import UsuarioPerfil, Calendario, Album, RelacionUsuario
from django.contrib.auth.models import User
import datetime


class RegistroUsuario(forms.Form):
    usuario = forms.CharField(max_length=50, label='Usuario')
    clave =  forms.CharField(max_length=20, widget=forms.PasswordInput,label='Clave')
    nombre =  forms.CharField(max_length=50, label='Nombre')
    apellido = forms.CharField(max_length=50, label='Apellido')
    nacimiento = forms.CharField(max_length=50, label='Nacimiento')
    direccion =  forms.CharField(max_length=50, label='Direccion')
    twitter =  forms.CharField(max_length=50, label='Twitter')
    facebook =  forms.CharField(max_length=50, label='Facebook')
    correo =  forms.CharField(max_length=50, label='Correo')
    privacidad =  forms.BooleanField(label='Privacidad')
    foto = forms.ImageField(label='Foto', required=False)    
    
    def __init__(self,*args, **kwargs):
        super(RegistroUsuario, self).__init__(*args, **kwargs)
        self.fields['usuario'].widget.attrs = {'placeholder': 'usuario', 'class': 'form-control'}
        self.fields['clave'].widget.attrs = {'placeholder': 'clave', 'class': 'form-control'}
        self.fields['nombre'].widget.attrs = {'placeholder': 'nombre', 'class': 'form-control'}
        self.fields['apellido'].widget.attrs = {'placeholder': 'apellido', 'class': 'form-control'}
        self.fields['nacimiento'].widget.attrs = {'placeholder': 'nacimiento', 'class': 'datepicker form-control'}
        self.fields['direccion'].widget.attrs = {'placeholder': 'direccion', 'class': 'form-control'}
        self.fields['twitter'].widget.attrs = {'placeholder': 'twitter', 'class': 'form-control'}
        self.fields['facebook'].widget.attrs = {'placeholder': 'facebook', 'class': 'form-control'}
        self.fields['correo'].widget.attrs = {'placeholder': 'correo', 'class': 'form-control'}
        #self.fields['privacidad'].widget.attrs = {'class': 'form-control'}
        self.fields['foto'].widget.attrs = {'placeholder': 'foto', 'class': 'form-control'}
   
    def clean_nacimiento(self):
        fecha = self.cleaned_data['nacimiento'].split('/')
        fecha = map(int, fecha)
        fecha = datetime.date(year=fecha[2], month=fecha[0], day=fecha[1])
        hoy = datetime.date.today()
        if fecha >= hoy:
            raise forms.ValidationError("Fecha de nacimiento, no puede ser mayor o igual a la de hoy")
        return fecha

    def clean_twitter(self):
        twitter = self.cleaned_data['twitter']
        if twitter.startswith('@'):
            return twitter
        raise forms.ValidationError("El campo no comienza con un @")
    
    def procesar_registro(self):
        username = self.cleaned_data['usuario']
        password = self.cleaned_data['clave']
        name = self.cleaned_data['nombre']
        lastname = self.cleaned_data['apellido']
        fechaNac = self.cleaned_data['nacimiento']
        direccion = self.cleaned_data['direccion']
        twitter = self.cleaned_data['twitter']
        facebook = self.cleaned_data['facebook']
        email = self.cleaned_data['correo']
        privacidad = self.cleaned_data['privacidad']
        foto = self.cleaned_data.get('foto', None)
        usuario = User(username=username, first_name=name, last_name=lastname, email=email)
        usuario.set_password(password)
        usuario.save()
        perfil = UsuarioPerfil(fechanacimiento=fechaNac, direccion=direccion, twitter=twitter, facebook=facebook, privacidad=privacidad, fkusuario=usuario)
        if foto:
            perfil.foto = foto
        perfil.save()

        
class EditarUsuario(RegistroUsuario):
    def __init__(self, *args, **kwargs):
        super(EditarUsuario, self).__init__(*args, **kwargs)
        self.fields['clave'].required = False
        
    def modificar_registro(self, usuario):
        (self.cleaned_data['clave'])
        usuario.first_name = self.cleaned_data['nombre']
        usuario.last_name = self.cleaned_data['apellido']
        usuario.usuarioperfil.fechanacimiento = self.cleaned_data['nacimiento']
        usuario.usuarioperfil.direccion = self.cleaned_data['direccion']
        usuario.usuarioperfil.twitter = self.cleaned_data['twitter']
        usuario.usuarioperfil.facebook = self.cleaned_data['facebook']
        usuario.email = self.cleaned_data['correo']
        usuario.usuarioperfil.privacidad = self.cleaned_data['privacidad']
        foto = self.cleaned_data.get('foto', None)
        if foto:
            usuario.usuarioperfil.foto = foto
        usuario.usuarioperfil.save()
        usuario.save()


#Formulario del Album
class RegistroAlbum(forms.Form):
    nombre = forms.CharField(max_length=50, label='Nombre')
    descripcion = forms.CharField(max_length=20,label='Descripcion')
    privacidad = forms.BooleanField(label='Privacidad', required=False)
    foto = forms.ImageField(label='Foto', required=False)   
   
    def __init__(self,*args, **kwargs):
        super(RegistroAlbum, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs = {'placeholder': 'nombre', 'class': 'form-control'}
        self.fields['descripcion'].widget.attrs = {'placeholder': 'descripcion', 'class': 'form-control'}
        self.fields['foto'].widget.attrs = {'placeholder': 'foto', 'class': 'form-control'}
        
    def procesar_album(self,usuario):
        nombre = self.cleaned_data['nombre']
        descripcion = self.cleaned_data['descripcion']
        privacidad = self.cleaned_data['privacidad']
        foto = self.cleaned_data['foto']
        calendar = Calendario(fecha=datetime.date.today())
        calendar.save()
        album = Album(nombre=nombre, descripcion=descripcion, privacidad=privacidad, fkusuario=usuario, fkcalendario=calendar)
        if foto:
            album.foto = foto
        album.save()

    def modificar_album(self, album):
        album.nombre = self.cleaned_data['nombre']
        album.descripcion = self.cleaned_data['descripcion']
        album.privacidad = self.cleaned_data['privacidad']
        foto = self.cleaned_data['foto']
        calendar = Calendario(fecha=datetime.date.today())
        calendar.save()
        if foto:
            album.foto = foto
        album.save()    

#Relacion Usuario
class RegistroAmigo(forms.Form):
    fkamigo = forms.IntegerField(label='Amigo')
    
    def __init__(self,*args, **kwargs):	
        super(RegistroAmigo, self).__init__(*args, **kwargs)
        self.fields['fkamigo'].widget.attrs = {'placeholder': 'fkamigo', 'class': 'form-control'}
        
    def procesar_amigo(self, usuario):
        id_amigo = self.cleaned_data['fkamigo']
        #import pdb; pdb.set_trace()
        id_usuario = UsuarioPerfil.objects.get(fkusuario=usuario)
        amigo = User.objects.get(id=id_amigo)
        amistad = RelacionUsuario(usuario=id_usuario, fkamigo=amigo)
        amistad.save()
        
