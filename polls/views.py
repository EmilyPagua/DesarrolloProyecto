#coding=utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from polls.forms import RegistroUsuario, EditarUsuario, RegistroAlbum, RegistroAmigo, RegistroFoto,RegistroComentario
from polls.models import UsuarioPerfil, Album ,Notificacion, Contenido, Historial, Contenido, Comentario
from django.contrib.auth.models import User
from django.db.models import Q



#Prueba
@login_required
def prueba(request,id_album):
    usuario = request.user    
    contexto = {'usuario' : usuario}
    return render_to_response('detalleAlbum.html',context_instance=RequestContext(request, contexto))    
	        
#---------------- C O M E N T A R I O S------------------
	        
#comentarios mios
@login_required
def comentario_Mio(request):
    usuario = request.user     
    usu = User.objects.get(id=usuario.id)
    comentario = Comentario.objects.filter(userComentador=usu.id)      
    contexto = {'usuario' : usuario, 'comentario':comentario }
    return render_to_response('MisComentarios.html',context_instance=RequestContext(request, contexto))    
    	        
   
#Mis comentarios
@login_required
def misComentarios(request,id_album):
    usuario = request.user        
    usu = User.objects.get(id=usuario.id)
    import pdb; pdb.set_trace() 
    print usu.id
    albu = get_object_or_404(Album, id=id_album)
    albumes = Album.objects.get(id=albu.id)    
    if request.method == 'POST':         
        formulario = RegistroComentario(request.POST)
        if formulario.is_valid():
            formulario.procesar_comentario(albumes,usu)
            comentarioPersona = Comentario.objects.filter(userComentador=usu.id)      
            contexto = {'usuario' : usuario, 'comentario':comentarioPersona }
            return render_to_response('MisComentarios.html',context_instance=RequestContext(request, contexto)) 
    
    contexto = {'usuario' : usuario, 'comentario':comentarioPersona() }
    return render_to_response('comentariosHechos.html',context_instance=RequestContext(request, contexto))    
            
	        
#---------------- U S U A R I O ------------------

#Pagina de inicio despues de login
@login_required
def principal_inicio(request):
    usuario = request.user
    historial =  Historial.objects.order_by('id').reverse()
    contenido = Contenido.objects.all()
    notificacion = Notificacion.objects.all()
    comentario = Comentario.objects.all()
    amigos = UsuarioPerfil.objects.filter(amigos=usuario.id)
    id_per = [amigo.id+1 for amigo in amigos] #lista por comprension
    persona = User.objects.filter(id__in=id_per)
    
    contexto = {'usuario': usuario, 'historial':historial,'contenido':contenido,'notificacion':notificacion, 'comentario':comentario,'persona':persona}
    return render_to_response('principalinicio.html',context_instance=RequestContext(request, contexto))


#Registrar Usuario
def registro_usuario(request):  
    if request.method == 'POST':
        formulario = RegistroUsuario(request.POST, request.FILES)
        if formulario.is_valid():
	        formulario.procesar_registro()
	        return HttpResponseRedirect(reverse('login'))   
    contexto = {'formulario': RegistroUsuario()}
    return render_to_response('usuarioRegistrar.html',context_instance=RequestContext(request, contexto))
	

#Modificar usuario
def modificar_usuario(request,id_usuario):    
    usuario = get_object_or_404(User, id=id_usuario)
    if request.method == 'POST':
        formulario = EditarUsuario(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.modificar_registro(usuario)           
    form_data = {        
        'nombre': usuario.first_name,
        'apellido' : usuario.last_name,
        'nacimiento' : '',
        'direccion' : usuario.usuarioperfil.direccion,        
        'facebook' : usuario.usuarioperfil.facebook,
        'correo' : usuario.email,
        'privacidad' : usuario.usuarioperfil.privacidad,
        'foto' : usuario.usuarioperfil.foto,
    }
    contexto = {'formulario': EditarUsuario(initial=form_data), 'usuario': usuario}
    return render_to_response('usuarioModificar.html',context_instance=RequestContext(request, contexto))


@login_required
def ver_MiPerfil(request,id_usuario):    
    usuario = request.user    
    amigos = UsuarioPerfil.objects.filter(amigos=usuario.id)
    id_per = [amigo.id+1 for amigo in amigos] #lista por comprension
    persona = User.objects.filter(id__in=id_per)
    
    usu = User.objects.filter(id=id_usuario)    
    albumes = Album.objects.filter(fkusuario=usuario)
    contexto = {'usuario': usuario, 'usu':usu,'albumes':albumes,'persona':persona}
    return render_to_response('verMiPerfil.html',context_instance=RequestContext(request,contexto))
 
#---------------- A L B U M E S ------------------

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



#Ver Albumes
@login_required
def ver_albumes(request):
    usuario = request.user
    albumes = Album.objects.filter(fkusuario=usuario)
    contexto = {'albumes': albumes,'usuario': usuario}
    return render_to_response('verAlbumes.html',context_instance=RequestContext(request,contexto))


 
#Detalle Mi Album (Va a detalle del album, modifica el album 
@login_required
def detalle_album(request,id_album):
    usuario = request.user
    albu = get_object_or_404(Album, id=id_album)
    albumes = Album.objects.filter(id=albu.id)
    contenido = Contenido.objects.filter(fkalbum=albu.id)
    comentarioAlbum = Comentario.objects.filter(fkalbum=albu.id)      
    cantidadComentario = Comentario.objects.filter(fkalbum=albu.id).count()                    
    #Modificar Album
    if 'modi' in request.POST:        
        form_data = {
            'nombre': albu.nombre,
            'descripcion': albu.descripcion,
            'privacidad' : albu.privacidad,
            'foto' : albu.foto,
   	    }
        contexto = {'formulario': RegistroAlbum(initial=form_data), 'usuario': usuario, 'album': albumes}
        return render_to_response('albumModificar.html',context_instance=RequestContext(request, contexto))    
    
    #Ver album, ver sus fotos y comentarios
    if 'ver' in request.POST:       
        contexto = {'usuario' : usuario, 'albumes' : albumes, 'contenido' : contenido, 'comentarioAlbum' : comentarioAlbum,'formulario': RegistroComentario(), 'cantidadComentario':cantidadComentario  }
        return render_to_response('detalleAlbum.html',context_instance=RequestContext(request, contexto)) 
    
    #Agregar fotos al album
    if 'acep' in request.POST:
        formulario = RegistroAlbum(request.POST, request.FILES)       
        if formulario.is_valid():
            formulario.modificar_album(albu)    	
            return HttpResponseRedirect(reverse('verAlbumes'))    
    
    #Eliminar el album
    if 'elimi' in request.POST:
        albumes.delete()
        return HttpResponseRedirect(reverse('verAlbumes'))  
            
            
    contexto = {'usuario' : usuario}
    return render_to_response('comentariosHechos.html',context_instance=RequestContext(request, contexto))    
	   
	        
  
  
#Detalle de los albumes de mis amigos (Se ven las fotos en el carrusel)
@login_required
def detalle_album2(request,id_album):
    usuario = request.user
    albu = get_object_or_404(Album, id=id_album)
    albumes = Album.objects.filter(id=albu.id)
    contenido = Contenido.objects.filter(fkalbum=albu.id)
    comentarioAlbum = Comentario.objects.filter(fkalbum=albu.id)      
    catidadComentario = Comentario.objects.filter(fkalbum=albu.id).count()       
    
    contexto = {'usuario' : usuario, 'albumes' : albumes, 'contenido' : contenido, 'comentarioAlbum' : comentarioAlbum, 'formulario' : RegistroComentario(),'catidadComentario':catidadComentario  }
    return render_to_response('detalleAlbum.html',context_instance=RequestContext(request, contexto))    
	
#agregarfotos
@login_required
def registro_foto(request,id_album):
    usuario = request.user
    albumes = Album.objects.filter(id=id_album)
    if request.method == 'POST':               
        #import pdb; pdb.set_trace()
        print request.POST 
        formulario =RegistroFoto(request.POST)
        if formulario.is_valid():
            print request.method    
            formulario.procesar_foto(usuario)
            return HttpResponseRedirect(reverse('principalInicio')) 

    #import pdb; pdb.set_trace()       
    contexto = {'usuario': usuario,'albumes':albumes }
    return render_to_response('agregarFotos.html',context_instance=RequestContext(request, contexto))


#---------------- N O T I F I C A C I O N E S ------------------

@login_required
def ver_notificacion(request):
    usuario = request.user    
    if 'aceptar' in request.POST:                     
        formulario = RegistroAmigo(request.POST)
        if formulario.is_valid():
            formulario.procesar_amigo(usuario)
            return HttpResponseRedirect(reverse('principalInicio')) 
            
    informacion = Notificacion.objects.filter(usuario=usuario)
    contexto = {'informacion': informacion,'usuario': usuario}
    return render_to_response('notificar.html',context_instance=RequestContext(request,contexto))


#Notificaciones Aprobadas
@login_required
def notificaciones_aprobadas(request,id_notificacion,id_amigo):
    usuario = request.user
    noti = get_object_or_404(Notificacion, id=id_notificacion)
    notifica = Notificacion.objects.filter(id=noti.id)
    notifica.update(status='true')
    informacion = Notificacion.objects.filter(usuario=usuario)    
    k = User.objects.get(id=usuario.id)
    l = User.objects.get(id=id_amigo)
    l.usuarioperfil.amigos.add(k)
    l.save()
    k.usuarioperfil.amigos.add(l)
    k.save()
    
    if 'aceptar' in request.POST:
        contexto = {'usuario' : usuario,'informacion':informacion }
        
        return render_to_response('verNotificacionesAceptadas.html',context_instance=RequestContext(request, contexto))    
    return HttpResponseRedirect(reverse('principalInicio')) 	        
   
 #Ver Todas la notificaciones Aceptadas
@login_required
def notificaciones_aceptadas(request):
    usuario = request.user
    albumes = Album.objects.filter(fkusuario=usuario)
    informacion = Notificacion.objects.filter(usuario=usuario)
    contexto = {'albumes': albumes,'usuario': usuario,'informacion':informacion}
    return render_to_response('NotificacionesAprobadas.html',context_instance=RequestContext(request,contexto))

#---------------- R E L A C I O N   A M I S T A D ------------------


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

        
#Ver Amigos ACOMODANDO
@login_required
def ver_amigos(request):        
    usuario = request.user
    amigos = UsuarioPerfil.objects.filter(amigos=usuario.id)
    id_per = [amigo.id+1 for amigo in amigos] #lista por comprension
    persona = User.objects.filter(id__in=id_per)
    contexto = {'persona': persona, 'usuario': usuario}
    return render_to_response('verAmigos.html',context_instance=RequestContext(request,contexto))


#Ver Amigos buscados
@login_required
def ver_usuario(request, nombre):
    usuario = request.user  
             
    if 'buscar' in request.POST:    
        #import pdb; pdb.set_trace()
        formulario = RegistroAmigo(request.POST)
        if formulario.is_valid():
            formulario.procesar_notificacion(usuario)
            return HttpResponseRedirect(reverse('principalInicio'))

    if 'enviar' in request.POST:            
        l = User.objects.get(username=nombre)
        k = User.objects.get(id=usuario.id)
        print l
        #llenar historial
        b = Historial(usuario=k, accion='Amistad')
        b.save()
        #llenar notificacion
        c = Notificacion(usuario=l, historia=b, descripcion ='Amistad')
        c.save()
        return HttpResponseRedirect(reverse('principalInicio'))
     
    nc = nombre.split(" ")    
    persona = User.objects.filter(first_name__regex = nombre)
    id_per = [amigo.id for amigo in persona] #lista por comprension    
    personitas = User.objects.filter(id__in=id_per)    
    contexto = {'usuario': usuario, 'perfil': personitas}
    return render_to_response('verUsuario.html',context_instance=RequestContext(request,contexto))


#Ver perfil Amigo
@login_required
def ver_PerfilAmigo(request,id_usuario):    
    usuario = request.user
    amigos = UsuarioPerfil.objects.filter(amigos=id_usuario)
    id_per = [amigo.id+1 for amigo in amigos] #lista por comprension
    persona = User.objects.filter(id__in=id_per)    
    usu = User.objects.filter(id=id_usuario)    
    albumes = Album.objects.filter(fkusuario=usu)
    contexto = {'usuario': usuario, 'usu':usu,'albumes':albumes,'persona':persona}
    return render_to_response('PerfilAmigo.html',context_instance=RequestContext(request,contexto))
 
 
#Buscador de Amigos
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
            nombre_completo = i.first_name 
            element = {"nombre":nombre_completo}
            objects.append(json.dumps(element))
            items = { "items" : objects}
    return HttpResponse(json.dumps(items),mimetype="text/plain")



