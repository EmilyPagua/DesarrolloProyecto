from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .forms import RegistroUsuario, EditarUsuario, RegistroAlbum, RegistroAmigo
from .models import UsuarioPerfil , Album , Calendario, RelacionUsuario
from django.contrib.auth.models import User
from django.db.models import Q



#Prueba
def prueba(request):
	return render_to_response('albumRegistrar.html',context_instance=RequestContext(request))

#Pagina de inicio despues de login
@login_required
def principal_inicio(request):
    usuario = request.user
    contexto = {'usuario': usuario}
    return render_to_response('principalinicio.html',context_instance=RequestContext(request, contexto))

#Modificar usuario
def modificar_usuario(request,id_usuario):    
    usuario = get_object_or_404(User, id=id_usuario)
    if request.method == 'POST':
        formulario = EditarUsuario(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.modificar_registro(usuario)           
    form_data = {
        'usuario': usuario.username,
        'nombre': usuario.first_name,
        'apellido' : usuario.last_name,
        'nacimiento' : usuario.usuarioperfil.fechanacimiento,
        'direccion' : usuario.usuarioperfil.direccion,
        'twitter' : usuario.usuarioperfil.twitter,
        'facebook' : usuario.usuarioperfil.facebook,
        'correo' : usuario.email,
        'privacidad' : usuario.usuarioperfil.privacidad,
        'foto' : usuario.usuarioperfil.foto,
    }
    contexto = {'formulario': EditarUsuario(initial=form_data), 'usuario': usuario}
    return render_to_response('usuarioModificar.html',context_instance=RequestContext(request, contexto))

#Modificar Album
@login_required
def modificar_album(request,id_album):
    usuario = request.user
    album = get_object_or_404(Album,id=id_album)
    if request.method == 'POST':
        formulario = RegistroAlbum(request.POST, request.FILES)       
        if formulario.is_valid():
            formulario.modificar_album(album)
            
    form_data = {
        'nombre': album.nombre,
        'descripcion': album.descripcion,
        'privacidad' : album.privacidad,
        'foto' : album.foto,
    }
    contexto = {'formulario': RegistroAlbum(initial=form_data), 'usuario': usuario, 'album': album}
    return render_to_response('albumModificar.html',context_instance=RequestContext(request, contexto))


#Registrar Usuario
def registro_usuario(request):
	if request.method == 'POST':
	    formulario = RegistroUsuario(request.POST, request.FILES)
	    if formulario.is_valid():
	        formulario.procesar_registro()
	contexto = {'formulario': RegistroUsuario()}
	return render_to_response('usuarioRegistrar.html',context_instance=RequestContext(request, contexto))
	

#Crear Album
@login_required
def registro_album(request): 
    usuario = request.user
    if request.method == 'POST':
        formulario = RegistroAlbum(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.procesar_album(usuario)
            return HttpResponseRedirect(reverse('principalInicio'))   
    contexto = {'formulario': RegistroAlbum(),'usuario': usuario}
    return render_to_response('albumRegistrar.html',context_instance=RequestContext(request, contexto))


#Ver Amigos
@login_required
def ver_amigos(request):
	
    usuario = request.user
    up = UsuarioPerfil.objects.get(fkusuario=usuario)
    amigos = RelacionUsuario.objects.filter(Q(usuario=usuario) | Q(fkamigo=up))
    id_per =[amigo.id for amigo in amigos] #lista por comprension
    persona = User.objects.filter(id__in=id_per)
    contexto = {'persona': persona, 'usuario': usuario}
    return render_to_response('verAmigos.html',context_instance=RequestContext(request,contexto))


#Ver Albumes
@login_required
def ver_albumes(request):
    usuario = request.user
    albumes = Album.objects.filter(fkusuario=usuario)
    contexto = {'albumes': albumes,'usuario': usuario}
    return render_to_response('verAlbumes.html',context_instance=RequestContext(request,contexto))

#Crear Relacion
@login_required
def registro_amigo(request): 
    usuario = request.user
    if request.method == 'POST':            
        formulario = RegistroAmigo(request.POST)
        if formulario.is_valid():
            formulario.procesar_amigo(usuario)
            return HttpResponseRedirect(reverse('principalInicio'))  
    formulario = RegistroAmigo()      
    contexto = {'usuario': usuario, 'perfil': perfil, 'formulario': formulario}
    return render_to_response('verUsuario.html',context_instance=RequestContext(request,contexto))

	
#Ver Amigo
@login_required
def ver_usuario(request, nombre):
    usuario = request.user
    if request.method == 'POST':            
        formulario = RegistroAmigo(request.POST)
       # import pdb; pdb.set_trace()

        if formulario.is_valid():
            formulario.procesar_amigo(usuario)
            return HttpResponseRedirect(reverse('principalInicio'))  
    
    nc = nombre.split(" ")
    n = nc[0]
    a = nc [1]
    persona = User.objects.filter(first_name=n, last_name=a)
    perfil= UsuarioPerfil.objects.filter(fkusuario=persona)

    formulario = RegistroAmigo()   
    #persona = User.objects.filter(=usuario)
    contexto = {'usuario': usuario, 'perfil': perfil,'formulario': formulario}
    return render_to_response('verUsuario.html',context_instance=RequestContext(request,contexto))

import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def busqueda(request):
 
    if request.method=='GET' or not request.POST.__contains__('start'):
        return HttpResponseForbidden()
 
    # Hacemos la consulta para aquellos elementos que empiecen por start ordenados por nombre
    query = User.objects.filter(first_name__istartswith=request.POST['start']).order_by('first_name')
 
    # Serializamos
    cont = 0
    objects = []
    for i in query:
    	nombre_completo = i.first_name + " " + i.last_name
    	element = {"nombre":nombre_completo}
    	objects.append(json.dumps(element))
 	items = { "items" : objects}
    return HttpResponse(json.dumps(items),mimetype="text/plain")
    

