#coding=utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from polls.forms import RegistroUsuario, EditarUsuario, RegistroAlbum, RegistroAmigo,RegistroComentario,BuscarHashtag
from polls.models import UsuarioPerfil, Album ,Notificacion, Contenido, Historial, Contenido, Comentario, Like
from django.contrib.auth.models import User
from django.db.models import Q





#***************************
#Prueba
@login_required
def prueba(request,id_album):
    usuario = request.user    
    contexto = {'usuario' : usuario}
    
# Leemos el contenido para comprobar que ha sobreescrito el contenido.
    infile = open('archivoLogs.txt', 'r')
    print('>>> Escritura de fichero concatenando su contenido.')
    #print(infile.read())
# Cerramos el fichero.
    infile.close() 
    return render_to_response('detalleAlbum.html',context_instance=RequestContext(request, contexto))    

	        
  
  

#---------------- I N S T A G R A M------------------
#hashtag 
@login_required
def agregarFoto(request,id_album):
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('AgregarFoto -- OBTENIENDO USUARIO QUE VA A AGREGAR FOTO AL ALBUM\n')    
    usuario = request.user
    albu = get_object_or_404(Album, id=id_album)
    albumes = Album.objects.get(id=albu.id) 
    if request.method == 'POST':
        p = request.POST['hashtag']
        contexto = {'usuario': usuario,'p':p,'albumes':albumes}
        outfile.write('agregarFoto -- OBTENIENDO USUARIO QUE VA A AGREGAR FOTO AL ALBUM\n')    
        outfile.close()
        return render_to_response('buscarHashtag.html',context_instance=RequestContext(request, contexto))

    contexto = {'usuario': usuario, 'formulario': BuscarHashtag(),'albumes':albumes}  
    outfile.write('agregarFoto -- OBTNIENDO LAS FOTOS QUE SON CAPTURADAS DEL INSTAGRAM\n')
    outfile.close()
    return render_to_response('agregarFotos.html',context_instance=RequestContext(request, contexto))


#paso de hashtag 
@login_required
def buscarHashtag(request):
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('buscarHashtag -- BUSCANDO IMAGENES EN INSTAGRAM\n')    
    usuario = request.user
    contexto = {'usuario': usuario, 'formulario': BuscarHashtag()}
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('buscarHashtag -- OBTENIENDO IMAGENES DEL INSTAGRAM\n')
    outfile.close()        
    return render_to_response('buscarHashtag.html',context_instance=RequestContext(request, contexto))


#Guardando Imagenes
@login_required
def guardarFoto(request,id_album):
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('guardarFoto -- OBTENIENDO NOMBRE DEL ALBUM EN DONDE SE VAN A GUARDAR LAS FOTOS\n')
    usuario = request.user
    albu = get_object_or_404(Album, id=id_album)
    if request.method == 'POST':
       outfile.write('guardarFoto -- GUARDANDO FOTOS EN UN ARREGLO PARA SER GUARDADAS EN EL MODEL CONTENIDO\n')
       imagenes = request.POST.getlist('imagenes[]')
       
    for imagen in imagenes: 
       contenido= Contenido(urlfoto=imagen,fkalbum=albu)
       outfile.write('guardarFoto -- GUARDANDO QUE SE OBTUVIERON DEL INSTAGRAM\n')
       contenido.save()     
    
    outfile.close()
    return HttpResponse(status=200) 
    
       
#---------------- C O M E N T A R I O S-----------------

#Enviar like comentario
@login_required
def Nolike(request,id_comentario):    
    usuario = request.user
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    comentario = get_object_or_404(Comentario, id=id_comentario)
    album = Album.objects.get(id=comentario.fkalbum.id)
    albumes = Album.objects.filter(id=album.id)
    usu = User.objects.get(id= comentario.fkalbum.fkusuario.id )
    contenido = Contenido.objects.filter(fkalbum=comentario.fkalbum.id)
    comentarioAlbum = Comentario.objects.filter(fkalbum=comentario.fkalbum.id)      
    cantidadComentario = Comentario.objects.filter(fkalbum=comentario.fkalbum.id).count()          
    cantidadLike = Like.objects.all()   
    count = Like.objects.filter(fkcomentario = comentario, userLike=usuario)
    if count:
    	for aux in count: 
            aux.delete()    	
    contexto = {'usuario' : usuario, 'albumes' : albumes, 'contenido' : contenido, 'comentarioAlbum' : comentarioAlbum,'formulario': RegistroComentario(), 'cantidadComentario':cantidadComentario ,'cantidadLike':cantidadLike }
    outfile.write('LikeComentario - OBTENIENDO USUARIO QUE HIZO LIKE\n')
    outfile.write('LikeComentario - ENVIANDO POR CONTEXTO AL: USUARIO, ALBUMES, CONTENIDO, COMENTARIO, FOMULARIO Y LIKE\n')
    outfile.close()
    return render_to_response('detalleAlbum.html',context_instance=RequestContext(request, contexto)) 




#Enviar Borrar Comentario
@login_required
def borrarComentario(request,id_comentario):    
    usuario = request.user
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('borrarComentario - BORRANDO COMENTARIO\n')
    outfile.write('borrarComentario - ENVIANDO POR CONTEXTO AL: USUARIO, ALBUMES, CONTENIDO, COMENTARIO, FOMULARIO Y LIKE\n')
    outfile.close()
    print "Id comentario"
    print id_comentario
    print "Borrando comentario"
    comentario = get_object_or_404(Comentario, id=id_comentario)
    album = Album.objects.get(id=comentario.fkalbum.id)
    count = Comentario.objects.get(id=id_comentario)
    print count.descripcion 
    count.delete()    	        		    
    albumes = Album.objects.filter(id=album.id)    
    contenido = Contenido.objects.filter(fkalbum=album.id)
    comentarioAlbum = Comentario.objects.filter(fkalbum=album.id)      
    cantidadComentario = Comentario.objects.filter(fkalbum=album.id).count()          
    cantidadLike = Like.objects.all()       
    contexto = {'usuario' : usuario, 'albumes' : albumes, 'contenido' : contenido, 'comentarioAlbum' : comentarioAlbum,'formulario': RegistroComentario(), 'cantidadComentario':cantidadComentario ,'cantidadLike':cantidadLike }
    return render_to_response('detalleAlbum.html',context_instance=RequestContext(request, contexto)) 


#Enviar like comentario
@login_required
def likeComentario(request,id_comentario):    
    usuario = request.user
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    comentario = get_object_or_404(Comentario, id=id_comentario)
    album = Album.objects.get(id=comentario.fkalbum.id)
    albumes = Album.objects.filter(id=album.id)
    usu = User.objects.get(id= comentario.fkalbum.fkusuario.id )
    contenido = Contenido.objects.filter(fkalbum=comentario.fkalbum.id)
    comentarioAlbum = Comentario.objects.filter(fkalbum=comentario.fkalbum.id)      
    cantidadComentario = Comentario.objects.filter(fkalbum=comentario.fkalbum.id).count()          
    cantidadLike = Like.objects.all()   
    count = Like.objects.filter(fkcomentario = comentario, userLike=usuario)
    if count:
    	for aux in count: 
            aux.delete()    	
    		
    Liked = Like(fkcomentario=comentario, userLike=usuario,like=True)        
    Liked.save()           
    l = Like.objects.get(fkcomentario = comentario, userLike=usuario)
    k = User.objects.get(id=album.fkusuario.id)
    b = Historial(usuario=k, accion='like',fklike=l)
    b.save()
    contexto = {'usuario' : usuario, 'albumes' : albumes, 'contenido' : contenido, 'comentarioAlbum' : comentarioAlbum,'formulario': RegistroComentario(), 'cantidadComentario':cantidadComentario ,'cantidadLike':cantidadLike }
    outfile.write('LikeComentario - OBTENIENDO USUARIO QUE HIZO LIKE\n')
    outfile.write('LikeComentario - ENVIANDO POR CONTEXTO AL: USUARIO, ALBUMES, CONTENIDO, COMENTARIO, FOMULARIO Y LIKE\n')
    outfile.close()
    return render_to_response('detalleAlbum.html',context_instance=RequestContext(request, contexto)) 


#Enviar Replicar Comentario
@login_required
def EscribirReplicaComentario(request,id_comentario):    
    usuario = request.user    
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('EscribirReplicaComentario -- OBTENIENDO EL ID DEL USUARIO QUE QUIERE REALIZAR UNA REPLICA EN ALGUN COMENTARIO\n')
    comentario = get_object_or_404(Comentario, id=id_comentario)        
    album = Album.objects.get(id=comentario.fkalbum.id)
    if request.method == 'POST':         
        formulario = RegistroComentario(request.POST)
        if formulario.is_valid():
            formulario.procesar_replica(album,usuario,comentario)
            
    albumes = Album.objects.filter(id=album.id)
    usu = User.objects.get(id= comentario.fkalbum.fkusuario.id )
    contenido = Contenido.objects.filter(fkalbum=album.id)
    comentarioAlbum = Comentario.objects.filter(fkalbum=album.id)      
    cantidadComentario = Comentario.objects.filter(fkalbum=album.id).count()          
    cantidadLike = Like.objects.all() 
    outfile.write('EscribirReplicaComentario -- OBTENIENDO LAS CONTENIDO, USUARIO, ALBUM, COMENTARIO Y LIKE PARA IR A DETALLEALBUM\n')   
    contexto = {'usuario' : usuario, 'albumes' : albumes, 'contenido' : contenido, 'comentarioAlbum' : comentarioAlbum,'formulario': RegistroComentario(), 'cantidadComentario':cantidadComentario ,'cantidadLike':cantidadLike }
    outfile.close()
    return render_to_response('detalleAlbum.html',context_instance=RequestContext(request, contexto)) 
        

#Replicar Comentario
@login_required
def replicarComentario(request,id_comentario):    
    usuario = request.user
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('replicarComentario -- GUARDANDO LA PREPLICA DEL COMENTARIO QUE SE HIZO\n')
    coment = Comentario.objects.filter(id=id_comentario)          
    contexto = {'usuario' : usuario, 'formulario': RegistroComentario(),'coment':coment }
    outfile.close()
    return render_to_response('ReplicarComentario.html',context_instance=RequestContext(request, contexto))

#comentarios mios
@login_required
def comentario_Mio(request):
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('comentario_Mio -- MUESTRA LOS COMENTARIOS DE LA PERSONA QUE ESTA LOGUEADA\n')
    outfile.close()
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
    
    #import pdb; pdb.set_trace()     
    albu = get_object_or_404(Album, id=id_album)
    albumes = Album.objects.get(id=albu.id)    
    if request.method == 'POST':         
        formulario = RegistroComentario(request.POST)
        if formulario.is_valid():            
            formulario.procesar_comentario(albumes,usu)
            comentarioPersona = Comentario.objects.filter(userComentador=usu.id)      
            albu = get_object_or_404(Album, id=id_album)
            albumes = Album.objects.filter(id=albu.id)
            contenido = Contenido.objects.filter(fkalbum=albu.id)
            comentarioAlbum = Comentario.objects.filter(fkalbum=albu.id)      
            catidadComentario = Comentario.objects.filter(fkalbum=albu.id).count()           
            contexto = {'usuario' : usuario, 'albumes' : albumes, 'contenido' : contenido, 'comentarioAlbum' : comentarioAlbum, 'formulario' : RegistroComentario(),'catidadComentario':catidadComentario  }
            return render_to_response('detalleAlbum.html',context_instance=RequestContext(request, contexto))                
            
    contexto = {'usuario' : usuario, 'comentario':comentarioPersona() }
    return render_to_response('comentariosHechos.html',context_instance=RequestContext(request, contexto))    
            
	        
#---------------- U S U A R I O ------------------

#Pagina de inicio despues de login
@login_required
def principal_inicio(request):
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.    
    usuario = request.user
    historial =  Historial.objects.order_by('id').reverse()
    contenido = Contenido.objects.all()
    notificacion = Notificacion.objects.all()
    comentario = Comentario.objects.all()
    amigos = UsuarioPerfil.objects.filter(amigos=usuario.id)
    id_per = [amigo.id+1 for amigo in amigos] #lista por comprension
    persona = User.objects.filter(id__in=id_per)
    liked = Like.objects.all()
    
    contexto = {'usuario': usuario, 'historial':historial,'contenido':contenido,'notificacion':notificacion, 'comentario':comentario,'persona':persona,'liked':liked}
    outfile.write('principal_inicio -- PAGINA INICIAL DEL SISTEMA, SE MUESTRA EL HISTORIAR GENERAN DE LOS USUARIOS DE SOCIALACE\n')
    outfile.close()
    return render_to_response('principalinicio.html',context_instance=RequestContext(request, contexto))


#Registrar Usuario
def registro_usuario(request): 
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('registro_usuario -- SE ESTA INGRESANDO LOS DATOS DEL USUARIO EN SISTEMA\n')
    outfile.close()    
    if request.method == 'POST':
        formulario = RegistroUsuario(request.POST, request.FILES)
        if formulario.is_valid():
	        formulario.procesar_registro()
	        return HttpResponseRedirect(reverse('login')) 
	          
    contexto = {'formulario': RegistroUsuario()}
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('registro_usuario -- SE ESTA INGRESANDO LOS DATOS DEL USUARIO EN SISTEMA\n')
    outfile.close()
    return render_to_response('usuarioRegistrar.html',context_instance=RequestContext(request, contexto))
	

#Modificar usuario
def modificar_usuario(request,id_usuario):    
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('modificar_usuario -- OBTENIENDO LOS DATOS DEL USUARIO PARA SER MODIFICADOS\n')
    outfile.close()    
    usuario = get_object_or_404(User, id=id_usuario)
    if request.method == 'POST':
        print request.POST['foto']
        formulario = EditarUsuario(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.modificar_registro(usuario)           
    form_data = {        
        'nombre': usuario.first_name,
        'apellido' : usuario.last_name,       
        'direccion' : usuario.usuarioperfil.direccion,        
        'facebook' : usuario.usuarioperfil.facebook,
        'correo' : usuario.email,
        'privacidad' : usuario.usuarioperfil.privacidad,
        'foto' : usuario.usuarioperfil.foto,
    }
    contexto = {'formulario': EditarUsuario(initial=form_data), 'usuario': usuario}
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('modificar_usuario -- SE ESTAN ENVIANDO LOS DATOS DEL USUARIO, PARA LUEGO SER MODIFICADOS EN EL SISTEMA\n')
    outfile.close()
    return render_to_response('usuarioModificar.html',context_instance=RequestContext(request, contexto))


@login_required
def ver_MiPerfil(request,id_usuario):    
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('ver_MiPerfil -- MOSTRANDO LOS DATOS BASICOS, DE ALBUMES Y DE AMISTAD QUE TIENE EL USUARIO LOGUEADO\n')
    outfile.close()  
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
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('registro_album -- OBTENIENDO LOS DATOS DEL NUEVO ALBUM DEL USUARIO LOGUEADO EN SISTEMA\n')
    outfile.close()
    usuario = request.user
    if request.method == 'POST':        
        formulario = RegistroAlbum(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.procesar_album(usuario)
            return HttpResponseRedirect(reverse('verAlbumes'))   
    contexto = {'formulario': RegistroAlbum(),'usuario': usuario}
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('registro_album -- YA SE REGISTRO AL ALBUN NUEVO DEL USUARIO\n')
    outfile.close()
    return render_to_response('albumRegistrar.html',context_instance=RequestContext(request, contexto))



#Ver Albumes
@login_required
def ver_albumes(request):
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('ver_albumes -- SE OBSERVAN LOS ALBUMES DEL USUARIO QUE ESTA LOGUEADO EN SISTEMA\n')
    outfile.close()
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
    cantidadLike = Like.objects.all() 
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('Detalle_album -- SE MUESTRA UN ALBUM EN OARTICULAR, JUNTO CON SUS COMENTARIOS, LIKE, Y REPLICAS DE COMENTARIOS\n')
    outfile.close()

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
        contexto = {'usuario' : usuario, 'albumes' : albumes, 'contenido' : contenido, 'comentarioAlbum' : comentarioAlbum,'formulario': RegistroComentario(), 'cantidadComentario':cantidadComentario,'cantidadLike':cantidadLike  }
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
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('detalle_album2 -- SE MUESTRA EL ALBUM DE OTRO USUARIO QUE NO ESTE LOGUEADO EN EL SISTEMA\n')
    outfile.close()
    usuario = request.user
    albu = get_object_or_404(Album, id=id_album)
    albumes = Album.objects.filter(id=albu.id)
    contenido = Contenido.objects.filter(fkalbum=albu.id)
    comentarioAlbum = Comentario.objects.filter(fkalbum=albu.id)      
    catidadComentario = Comentario.objects.filter(fkalbum=albu.id).count()           
    contexto = {'usuario' : usuario, 'albumes' : albumes, 'contenido' : contenido, 'comentarioAlbum' : comentarioAlbum, 'formulario' : RegistroComentario(),'catidadComentario':catidadComentario  }
    return render_to_response('detalleAlbum.html',context_instance=RequestContext(request, contexto))    
	

#---------------- N O T I F I C A C I O N E S ------------------

@login_required
def ver_notificacion(request):
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('Mostrando notificaciones...\n')
    outfile.close()
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
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('notificaciones_aprobadas -- SE MUESTRAN LAS NOTIFICACIONES QUE TIENE EL USUARIO DISPONIBLE\n')
    outfile.close()
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
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('notificaciones_aceptadas -- NOTIFICACIONES QUE USUARIO A ACEPTADO, ESTA NOTIFICACIONES SON DE AMISTAD\n')
    outfile.close()
    usuario = request.user
    albumes = Album.objects.filter(fkusuario=usuario)
    informacion = Notificacion.objects.filter(usuario=usuario)
    contexto = {'albumes': albumes,'usuario': usuario,'informacion':informacion}
    return render_to_response('NotificacionesAprobadas.html',context_instance=RequestContext(request,contexto))



#---------------- R E L A C I O N   A M I S T A D ------------------

#Crear Relacion
@login_required
def registro_amigo(request):
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('registro_amigo -- SE HACE LA RELACION DE AMISTAD DE LOS USUARIOS QUE LE HAN PEDIDO AMISTAD, POR AQUI PASA SI EL HA ACEPTADO LA NOTIFICACION\n')
    outfile.close()
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
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('ver_amigos -- SE VEN LOS USUARIOS QUE TENGAS UNA RELACION DE AMISTAD CON EL USUARIO QUE ESTA LOGUEADO EN EL SISTEMA\n')
    outfile.close() 
    usuario = request.user
    amigos = UsuarioPerfil.objects.filter(amigos=usuario.id)
    id_per = [amigo.id+1 for amigo in amigos] #lista por comprension
    persona = User.objects.filter(id__in=id_per)
    contexto = {'persona': persona, 'usuario': usuario}
    return render_to_response('verAmigos.html',context_instance=RequestContext(request,contexto))


#Ver Amigos buscados
@login_required
def ver_usuario(request, nombre):
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('ver_usuario -- SE VEN LOS USUARIOS QUE FUERON OBTENIDOS EN EL BUSCADOR DE AMIGOS\n')
    outfile.close()
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
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('ver_PerfilAmigo -- MOSTRANDO PERLFIL COMPLETO DE LOS AMIGOS DE LA PERONSA QUE ESTA LOGUEADA\n')
    outfile.close()
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
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('busqueda -- BUSCANDO PEROSNA EN EL BUSCADOR\n')
    outfile.close()
    
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



