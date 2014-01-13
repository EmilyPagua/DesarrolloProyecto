#coding=utf-8
import re
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from polls.forms import RegistroUsuario, EditarUsuario, RegistroAlbum, RegistroAmigo,RegistroComentario,BuscarHashtag
from polls.models import UsuarioPerfil, Album ,Notificacion, Contenido, Historial, Contenido, Comentario, Like
from django.contrib.auth.models import User
from django.db.models import Q




#---------------- C O N T E N I D O ------------------
#hashtag 
@login_required
def agregarFoto(request,id_album):
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.    
    usuario = request.user
    albu = get_object_or_404(Album, id=id_album)
    albumes = Album.objects.get(id=albu.id) 
    if request.method == 'POST':
        p = request.POST['hashtag']
        contexto = {'usuario': usuario,'p':p,'albumes':albumes}
        outfile.write('agregarFoto -- USER:'+ usuario.username +' NAME: '+ usuario.first_name + ' LASTNAME: ' + usuario.last_name + '\n')    
        outfile.close()
        return render_to_response('buscarHashtag.html',context_instance=RequestContext(request, contexto))

    contexto = {'usuario': usuario, 'formulario': BuscarHashtag(),'albumes':albumes}  
    outfile.write('agregarFoto -- USER:'+ usuario.username +' NAME: '+ usuario.first_name + ' LASTNAME: ' + usuario.last_name +' OBTENIENDO LAS FOTOS QUE SON CAPTURADAS DEL INSTAGRAM, SOUNDCLOUD, YOUTUBE\n')
    outfile.close()
    return render_to_response('agregarFotos.html',context_instance=RequestContext(request, contexto))


#paso de hashtag 
@login_required
def buscarHashtag(request):
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.    
    usuario = request.user
    contexto = {'usuario': usuario, 'formulario': BuscarHashtag()}
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('buscarHashtag --USER:'+ usuario.username +' NAME: '+ usuario.first_name + ' LASTNAME: ' + usuario.last_name +' OBTENIENDO IMAGENES DEL INSTAGRAM, SOUNDCLOUD, YOUTUBE\n')
    outfile.close()        
    return render_to_response('buscarHashtag.html',context_instance=RequestContext(request, contexto))


#Guardando Imagenes
@login_required
def guardarFoto(request,id_album):
    outfile = open('archivoLogs.txt', 'a')     
    usuario = request.user
    albu = get_object_or_404(Album, id=id_album)
    if request.method == 'POST':
        outfile.write('guardarFoto -- USER:'+ usuario.username +' NAME: '+ usuario.first_name + ' LASTNAME: ' + usuario.last_name +' OBTENIENDO LOS ARREGLOS DEL CONTENIDO\n')
        imagenes = request.POST.getlist('imagenes[]')
     	videos = request.POST.getlist('videos[]')

    for imagen in imagenes: 
      
        if re.match("http://api.soundcloud", imagen):
   	        print "audio----"
   	        contenido= Contenido(urlaudio=imagen,fkalbum=albu)       

        if re.match("http://distilleryimage", imagen):
   	        print "imagen"
   	        contenido= Contenido(urlfoto=imagen,fkalbum=albu)       
   	        
        outfile.write('guardarFoto -- USER:'+ usuario.username +' NAME: '+ usuario.first_name + ' LASTNAME: ' + usuario.last_name +' GUARDANDO CONTENIDO'+ imagen +'\n')
        contenido.save()     
        
    for video in videos: 
        print "video"
        contenido2= Contenido(urlvideo=video,fkalbum=albu)         
        outfile.write('guardarFoto -- USER:'+ usuario.username +' NAME: '+ usuario.first_name + ' LASTNAME: ' + usuario.last_name +' GUARDANDO CONTENIDO'+ video +'\n')
        contenido2.save() 
    
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
    contenidofoto = Contenido.objects.filter(urlfoto__stloartswith="http://distilleryimage", fkalbum=album.id)    
    contenidoaudio = Contenido.objects.filter(urlaudio__startswith="http://api.soundcloud" , fkalbum=album.id) 
    contenidovideo = Contenido.objects.filter(urlvideo__startswith="http://www.youtube.com", fkalbum=album.id)     
    count = Like.objects.filter(fkcomentario = comentario, userLike=usuario)
    if count:
    	for aux in count: 
            aux.delete()    	
    contexto = {'usuario' : usuario, 'albumes' : albumes, 'comentarioAlbum' : comentarioAlbum,'formulario': RegistroComentario(), 'cantidadComentario':cantidadComentario ,'cantidadLike':cantidadLike,'contenidofoto':contenidofoto , 'contenidoaudio':contenidoaudio, 'contenidovideo':contenidovideo }    
    outfile.write('LikeComentario - USER:'+ usuario.username +' NAME: '+ usuario.first_name + ' LASTNAME: ' + usuario.last_name +' NO LE GUSTA EL COMENTARIO: '+ comentario.descripcion +' ALBUM: '+ album.nombre +'\n')
    outfile.close()
    return render_to_response('detalleAlbum.html',context_instance=RequestContext(request, contexto)) 



#Enviar Borrar Comentario
@login_required
def borrarComentario(request,id_comentario):    
    usuario = request.user
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.        
    comentario = get_object_or_404(Comentario, id=id_comentario)
    album = Album.objects.get(id=comentario.fkalbum.id)
    count = Comentario.objects.get(id=id_comentario)
    outfile.write('borrarComentario - USER:'+ usuario.username +' NAME: '+ usuario.first_name + ' LASTNAME: ' + usuario.last_name +' BORRANDO COMENTARIO: '+ count.descripcion+' DEL ALBUM: '+ album.nombre +'\n')
    count.delete()    	        		    
    albumes = Album.objects.filter(id=album.id)    
    contenido = Contenido.objects.filter(fkalbum=album.id)
    comentarioAlbum = Comentario.objects.filter(fkalbum=album.id)      
    cantidadComentario = Comentario.objects.filter(fkalbum=album.id).count()          
    cantidadLike = Like.objects.all()    
    contenidofoto = Contenido.objects.filter(urlfoto__startswith="http://distilleryimage", fkalbum=album.id)
    contenidoaudio = Contenido.objects.filter(urlaudio__startswith="http://api.soundcloud", fkalbum=album.id)
    contenidovideo = Contenido.objects.filter(urlvideo__startswith="http://www.youtube.com", fkalbum=album.id)             
    contexto = {'usuario' : usuario, 'albumes' : albumes, 'comentarioAlbum' : comentarioAlbum,'formulario': RegistroComentario(), 'cantidadComentario':cantidadComentario ,'cantidadLike':cantidadLike,'contenidofoto':contenidofoto ,'contenidoaudio':contenidoaudio , 'contenidovideo':contenidovideo }    
    outfile.close()    
    return render_to_response('detalleAlbum.html',context_instance=RequestContext(request, contexto)) 


#Enviar like comentario
@login_required
def likeComentario(request,id_comentario):        
    usuario = request.user
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    comentario = get_object_or_404(Comentario, id=id_comentario)
    album = Album.objects.get(id=comentario.fkalbum.id)
    albumes = Album.objects.filter(id=album.id)
    usu = User.objects.get(id= usuario.id )
    contenido = Contenido.objects.filter(fkalbum=comentario.fkalbum.id)
    comentarioAlbum = Comentario.objects.filter(fkalbum=comentario.fkalbum.id)      
    cantidadComentario = Comentario.objects.filter(fkalbum=comentario.fkalbum.id).count()          
    cantidadLike = Like.objects.all()   
    count = Like.objects.filter(fkcomentario = comentario, userLike=usuario)
    contenidofoto = Contenido.objects.filter(urlfoto__startswith="http://distilleryimage", fkalbum=album.id)
    contenidoaudio = Contenido.objects.filter(urlaudio__startswith="http://api.soundcloud", fkalbum=album.id) 
    contenidovideo = Contenido.objects.filter(urlvideo__startswith="http://www.youtube.com", fkalbum=album.id)           
    if count:
    	for aux in count: 
            aux.delete()    	
    		
    Liked = Like(fkcomentario=comentario, userLike=usuario,like=True)        
    Liked.save()           
    l = Like.objects.get(fkcomentario = comentario, userLike=usuario)
    k = User.objects.get(id=album.fkusuario.id)
    #llenar historial
    b = Historial(usuario=usu, accion='like',fklike=l)
    b.save()
    #llenar notificacion
    if not re.match(k.username, usu.username):    	
    	c = Notificacion(usuario=k, historia=b, descripcion ='Le dio like a tu Comentario: ' + comentario.descripcion)
        c.save()
    
    contexto = {'usuario' : usuario, 'albumes' : albumes, 'comentarioAlbum' : comentarioAlbum,'formulario': RegistroComentario(), 'cantidadComentario':cantidadComentario ,'cantidadLike':cantidadLike, 'contenidofoto':contenidofoto , 'contenidoaudio':contenidoaudio , 'contenidovideo':contenidovideo }    
    outfile.write('LikeComentario - ENVIANDO POR CONTEXTO AL: USUARIO, ALBUMES, CONTENIDO, COMENTARIO, FOMULARIO Y LIKE\n')
    outfile.close()
    return render_to_response('detalleAlbum.html',context_instance=RequestContext(request, contexto)) 


#Enviar Replicar Comentario
@login_required
def EscribirReplicaComentario(request,id_comentario):    
    usuario = request.user    
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.    
    comentario = get_object_or_404(Comentario, id=id_comentario)        
    album = Album.objects.get(id=comentario.fkalbum.id)
    contenidofoto = Contenido.objects.filter(urlfoto__startswith="http://distilleryimage", fkalbum=album.id)
    contenidoaudio = Contenido.objects.filter(urlaudio__startswith="http://api.soundcloud", fkalbum=album.id) 
    contenidovideo = Contenido.objects.filter(urlvideo__startswith="http://www.youtube.com", fkalbum=album.id)     
    
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
    outfile.write('EscribirReplicaComentario -- USER:'+ usuario.username +' NAME: '+ usuario.first_name + ' LASTNAME: ' + usuario.last_name +' REPLICO EL COMENTARIO: '+ comentario.descripcion +' DEL ALBUM: '+ album.nombre+'\n')   
    
    contexto = {'usuario' : usuario, 'albumes' : albumes, 'comentarioAlbum' : comentarioAlbum,'formulario': RegistroComentario(), 'cantidadComentario':cantidadComentario ,'cantidadLike':cantidadLike, 'contenidofoto':contenidofoto, 'contenidoaudio':contenidoaudio, 'contenidovideo':contenidovideo }
    outfile.close()
    return render_to_response('detalleAlbum.html',context_instance=RequestContext(request, contexto)) 
        

#Replicar Comentario
@login_required
def replicarComentario(request,id_comentario):    
    usuario = request.user
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.    
    coment = Comentario.objects.filter(id=id_comentario)          
    contexto = {'usuario' : usuario, 'formulario': RegistroComentario(),'coment':coment }
    outfile.write('replicarComentario -- USER:'+ usuario.username +' NAME: '+ usuario.first_name + ' LASTNAME: ' + usuario.last_name +' GUARDANDO LA PREPLICA DEL COMENTARIO: '+ coment.descripcion +' \n')
    outfile.close()
    return render_to_response('ReplicarComentario.html',context_instance=RequestContext(request, contexto))

#comentarios mios
@login_required
def comentario_Mio(request):
    usuario = request.user     
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('comentario_Mio -- USER:'+ usuario.username +' NAME: '+ usuario.first_name + ' LASTNAME: ' + usuario.last_name +', SE MOSTRARAN SUS COMENTARIOS\n')
    outfile.close()
    usu = User.objects.get(id=usuario.id)
    comentario = Comentario.objects.filter(userComentador=usu.id)      
    contexto = {'usuario' : usuario, 'comentario':comentario }
    return render_to_response('MisComentarios.html',context_instance=RequestContext(request, contexto))    
    	        
   
#Mis comentarios
@login_required
def misComentarios(request,id_album):
    usuario = request.user        
    usu = User.objects.get(id=usuario.id)        
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
            cantidadComentario = Comentario.objects.filter(fkalbum=albu.id).count()           
            contenidofoto = Contenido.objects.filter(urlfoto__startswith="http://distilleryimage", fkalbum=albu.id)
            contenidoaudio = Contenido.objects.filter(urlaudio__startswith="http://api.soundcloud", fkalbum=albu.id)  
            contenidovideo = Contenido.objects.filter(urlvideo__startswith="http://www.youtube.com", fkalbum=albu.id)        
            contexto = {'usuario' : usuario, 'albumes' : albumes, 'comentarioAlbum' : comentarioAlbum, 'formulario' : RegistroComentario(),'cantidadComentario':cantidadComentario, 'contenidofoto':contenidofoto, 'contenidoaudio':contenidoaudio, 'contenidovideo':contenidovideo   }
            return render_to_response('detalleAlbum.html',context_instance=RequestContext(request, contexto))                
            
    contexto = {'usuario' : usuario, 'comentario':comentarioPersona() }
    return render_to_response('comentariosHechos.html',context_instance=RequestContext(request, contexto))    
            
	        
#---------------- U S U A R I O ------------------

#Pagina de inicio despues de login
@login_required
def principal_inicio(request):
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.    
    usuario = request.user
    historial =  Historial.objects.order_by('id').reverse() #este es el historial
    contenido = Contenido.objects.all()
    notificacion = Notificacion.objects.all()
    comentario = Comentario.objects.all()
    amigos = UsuarioPerfil.objects.filter(amigos=usuario.id)    
    id_per = [amigo.id+1 for amigo in amigos] #lista por comprension
    Amigopersona = User.objects.filter(id__in=id_per) #estos son los usuarios amigos
    liked = Like.objects.all()
    contexto = {'usuario': usuario, 'historial':historial,'contenido':contenido,'notificacion':notificacion, 'comentario':comentario,'persona':Amigopersona,'liked':liked}
    outfile.write('principal_inicio -- USER:'+ usuario.username +' NAME: '+ usuario.first_name + ' LASTNAME: ' + usuario.last_name +'.\n')
    outfile.close()
    return render_to_response('principalinicio.html',context_instance=RequestContext(request, contexto))


#Registrar Usuario
def registro_usuario(request): 
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.    
    if request.method == 'POST':
        formulario = RegistroUsuario(request.POST, request.FILES)
        if formulario.is_valid():	        
	        contusu = User.objects.filter(username=request.POST['usuario']).count()	        
	        if contusu:	            
	            mensaje = "El usuario ya existe, ingrese otro nombre de usuario."
	            contexto = {'formulario':RegistroUsuario() ,'mensaje':mensaje}
	            return render_to_response('usuarioRegistrar.html',context_instance=RequestContext(request, contexto))	       	        
	            
	        formulario.procesar_registro()
	        return HttpResponseRedirect(reverse('login')) 
	          
    contexto = {'formulario': RegistroUsuario()}    
    outfile.write('registro_usuario --  SE ESTA INGRESANDO LOS DATOS DEL USUARIO EN SISTEMA\n')
    outfile.close()
    return render_to_response('usuarioRegistrar.html',context_instance=RequestContext(request, contexto))
	

#Modificar usuario
def modificar_usuario(request,id_usuario):    
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.    
    usuario = get_object_or_404(User, id=id_usuario)
    if request.method == 'POST':
        
        formulario = EditarUsuario(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.modificar_registro(usuario)                 
            amigos = UsuarioPerfil.objects.filter(amigos=usuario.id)
            id_per = [amigo.id+1 for amigo in amigos] #lista por comprension
            persona = User.objects.filter(id__in=id_per)
            usu = User.objects.filter(id=id_usuario)    
            albumes = Album.objects.filter(fkusuario=usuario)
            contexto = {'usuario': usuario, 'usu':usu,'albumes':albumes,'persona':persona}
            outfile.write('modificar_usuario -- USER: '+ usuario.username +' NAME:'+ usuario.first_name + ' LASTNAME:' + usuario.last_name + ', SE ESTAN ENVIANDO LOS DATOS DEL USUARIO PARA SER\n')
            outfile.close()
    	    return render_to_response('verMiPerfil.html',context_instance=RequestContext(request,contexto))          
            
    form_data = {        
        'nombre': usuario.first_name,
        'apellido' : usuario.last_name,       
        'direccion' : usuario.usuarioperfil.direccion,        
        'facebook' : usuario.usuarioperfil.facebook,
        'correo' : usuario.email,
        'privacidad' : usuario.usuarioperfil.privacidad,       
    }
    contexto = {'formulario': EditarUsuario(initial=form_data), 'usuario': usuario}    
    return render_to_response('usuarioModificar.html',context_instance=RequestContext(request, contexto))


@login_required
def ver_MiPerfil(request,id_usuario):    
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.         
    usuario = request.user    
    amigos = UsuarioPerfil.objects.filter(amigos=usuario.id)
    id_per = [amigo.id+1 for amigo in amigos] #lista por comprension
    persona = User.objects.filter(id__in=id_per)
    usu = User.objects.filter(id=id_usuario)    
    albumes = Album.objects.filter(fkusuario=usuario)
    contexto = {'usuario': usuario, 'usu':usu,'albumes':albumes,'persona':persona}
    outfile.write('ver_MiPerfil -- USER:'+ usuario.username +' NAME:'+ usuario.first_name + ' LASTNAME:' + usuario.last_name + ', VER DATOS BASICOS, DE ALBUMES Y DE AMISTAD\n')
    outfile.close() 
    return render_to_response('verMiPerfil.html',context_instance=RequestContext(request,contexto))
 
#---------------- A L B U M E S ------------------

#Crear Album
@login_required
def registro_album(request): 
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.       
    usuario = request.user
    if request.method == 'POST':        
        formulario = RegistroAlbum(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.procesar_album(usuario)
            return HttpResponseRedirect(reverse('verAlbumes'))   
    contexto = {'formulario': RegistroAlbum(),'usuario': usuario}   
    outfile.write('registro_album -- USER:'+ usuario.username +' NAME:'+ usuario.first_name + ' LASTNAME:' + usuario.last_name + ' YA SE REGISTRO NUEVO ALBUM\n')
    outfile.close()
    return render_to_response('albumRegistrar.html',context_instance=RequestContext(request, contexto))



#Ver Albumes
@login_required
def ver_albumes(request):
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.       
    usuario = request.user
    albumes = Album.objects.filter(fkusuario=usuario)
    contexto = {'albumes': albumes,'usuario': usuario}
    outfile.write('ver_albumes -- USER:'+ usuario.username +' NAME:'+ usuario.first_name + ' LASTNAME:' + usuario.last_name + ', SE OBSERVAN TODOS SUS ALBUMES\n')
    outfile.close()
    return render_to_response('verAlbumes.html',context_instance=RequestContext(request,contexto))


#Detalle Mi Album (Va a detalle del album, modifica el album 
@login_required
def detalle_album(request,id_album):
    usuario = request.user
    albu = get_object_or_404(Album, id=id_album)
    albumes = Album.objects.filter(id=albu.id)
    contenidofoto = Contenido.objects.filter(urlfoto__startswith="http://distilleryimage", fkalbum=albu.id)
    contenidoaudio = Contenido.objects.filter(urlaudio__startswith="http://api.soundcloud", fkalbum=albu.id)
    contenidovideo = Contenido.objects.filter(urlvideo__startswith="http://www.youtube.com", fkalbum=albu.id)    
    comentarioAlbum = Comentario.objects.filter(fkalbum=albu.id)      
    cantidadComentario = Comentario.objects.filter(fkalbum=albu.id).count()                    
    cantidadLike = Like.objects.all()     
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    outfile.write('Detalle_album -- USER:'+ usuario.username +' NAME:'+ usuario.first_name + ' LASTNAME:' + usuario.last_name + ', SE MUESTRA UN ALBUM: '+ albu.nombre +', JUNTO CON SUS COMENTARIOS, LIKE, Y REPLICAS DE COMENTARIOS\n')
    outfile.close()
   
    #Modificar Album
    if 'modi' in request.POST:        
        form_data = {
            'nombre': albu.nombre,
            'descripcion': albu.descripcion,
            'privacidad' : albu.privacidad,           
   	    }
        contexto = {'formulario': RegistroAlbum(initial=form_data), 'usuario': usuario, 'albu': albu, 'contenidofoto':contenidofoto, 'contenidoaudio':contenidoaudio, 'contenidovideo':contenidovideo }
        return render_to_response('albumModificar.html',context_instance=RequestContext(request, contexto))    
    
    #Ver album, ver sus fotos y comentarios
    if 'ver' in request.POST:       
        contexto = {'usuario' : usuario, 'albumes' : albumes, 'comentarioAlbum' : comentarioAlbum,'formulario': RegistroComentario(), 'cantidadComentario':cantidadComentario, 'cantidadLike':cantidadLike, 'contenidoaudio':contenidoaudio, 'contenidofoto' : contenidofoto, 'contenidovideo':contenidovideo }
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
    usuario = request.user
    albu = get_object_or_404(Album, id=id_album)
    albumes = Album.objects.filter(id=albu.id)
    contenidofoto = Contenido.objects.filter(urlfoto__startswith="http://distilleryimage", fkalbum=albu.id)
    contenidoaudio = Contenido.objects.filter(urlaudio__startswith="http://api.soundcloud", fkalbum=albu.id)
    contenidovideo = Contenido.objects.filter(urlvideo__startswith="http://www.youtube.com", fkalbum=albu.id)        
    contenido = Contenido.objects.filter(fkalbum=albu.id)
    comentarioAlbum = Comentario.objects.filter(fkalbum=albu.id)    
    cantidadLike = Like.objects.all()   
    outfile.write('detalle_album2 --  USER:'+ usuario.username +' NAME:'+ usuario.first_name + ' LASTNAME:' + usuario.last_name + ', SE MUESTRA EL ALBUM DE OTRO USUARIO QUE NO ESTE LOGUEADO EN EL SISTEMA\n')
    outfile.close()
    cantidadComentario = Comentario.objects.filter(fkalbum=albu.id).count()           
    contexto = {'usuario' : usuario, 'albumes' : albumes, 'comentarioAlbum' : comentarioAlbum, 'formulario' : RegistroComentario(),'cantidadComentario':cantidadComentario, 'contenidoaudio':contenidoaudio, 'contenidofoto' : contenidofoto, 'contenidovideo':contenidovideo ,'cantidadLike':cantidadLike }
    return render_to_response('detalleAlbum.html',context_instance=RequestContext(request, contexto))    
	

#eliminar contenido: foto, audio y video
@login_required
def eliminarContenido(request,id_contenido):   
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.    
    usuario = request.user
    contenido = get_object_or_404(Contenido, id=id_contenido)
    albu = Album.objects.get(id=contenido.fkalbum.id) 
    outfile.write('eliminarContenido --  USER:'+ usuario.username +' NAME:'+ usuario.first_name + ' LASTNAME:' + usuario.last_name + ',  SE ELIMINARA EL CONTENDO '+contenido.id+' DEL ALBUM: '+albu.nombre+'\n')    

    contenidofoto = Contenido.objects.filter(urlfoto__startswith="http://distilleryimage", fkalbum=albu.id)
    contenidoaudio = Contenido.objects.filter(urlaudio__startswith="http://api.soundcloud", fkalbum=albu.id)
    contenidovideo = Contenido.objects.filter(urlvideo__startswith="http://www.youtube.com", fkalbum=albu.id)    
    
    form_data = {
            'nombre': albu.nombre,
            'descripcion': albu.descripcion,
            'privacidad' : albu.privacidad,           
   	    }    
    contenido.delete()    
    contexto = {'formulario': RegistroAlbum(initial=form_data), 'usuario': usuario, 'albu': albu, 'contenidofoto':contenidofoto, 'contenidoaudio':contenidoaudio,'contenidovideo':contenidovideo }
    outfile.write('eliminarContenido -- Elimando el contenido\n')
    outfile.close()
    return render_to_response('albumModificar.html',context_instance=RequestContext(request, contexto))    
    
#eliminar contenido: foto, audio y video
@login_required
def ModificarAlbum(request,id_album):   
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.    
    usuario = request.user
    albu = Album.objects.get(id=id_album) 
    outfile.write('eliminarContenido --  USER:'+ usuario.username +' NAME:'+ usuario.first_name + ' LASTNAME:' + usuario.last_name + ',  SE VA A MODIFICAR EL ALBUM: '+ albu.nombre +'\n')    
    contenidofoto = Contenido.objects.filter(urlfoto__startswith="http://distilleryimage", fkalbum=albu.id)
    contenidoaudio = Contenido.objects.filter(urlaudio__startswith="http://api.soundcloud", fkalbum=albu.id)
    contenidovideo = Contenido.objects.filter(urlvideo__startswith="http://www.youtube.com", fkalbum=albu.id)    
    form_data = {
            'nombre': albu.nombre,
            'descripcion': albu.descripcion,
            'privacidad' : albu.privacidad,           
   	    }      
    contexto = {'formulario': RegistroAlbum(initial=form_data), 'usuario': usuario, 'albu': albu, 'contenidofoto':contenidofoto, 'contenidoaudio':contenidoaudio, 'contenidovideo':contenidovideo }   
    outfile.close()
    return render_to_response('albumModificar.html',context_instance=RequestContext(request, contexto))    
   
   
#---------------- N O T I F I C A C I O N E S ------------------

@login_required
def ver_notificacion(request):
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    usuario = request.user    
    outfile.write('ver_notificacion -- USER:'+ usuario.username +' NAME:'+ usuario.first_name + ' LASTNAME:' + usuario.last_name + ', SE MUESTRAN TODAS SUS NOTIFICACIONES\n')
    outfile.close()

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
    usuario = request.user
    noti = get_object_or_404(Notificacion, id=id_notificacion)
    notifica = Notificacion.objects.filter(id=noti.id)
    informacion = Notificacion.objects.filter(usuario=usuario)       
    outfile.write('notificaciones_aprobadas -- USER:'+ usuario.username +' NAME:'+ usuario.first_name + ' LASTNAME:' + usuario.last_name + ', SE MUESTRAN LAS NOTIFICACIONES HAN SIDO APROBADAS\n')
    outfile.close()
    
    if 'aceptar' in request.POST:
        notifica.update(status='true')        
        k = User.objects.get(id=usuario.id)
        l = User.objects.get(id=id_amigo)
        l.usuarioperfil.amigos.add(k)
        l.save()
        k.usuarioperfil.amigos.add(l)
        k.save()
        contexto = {'usuario' : usuario,'informacion':informacion }
        return render_to_response('verNotificacionesAceptadas.html',context_instance=RequestContext(request, contexto))    
            
    if 'rechazar' in request.POST:
        print "Rechazar"
        noti.delete() 
        contexto = {'usuario' : usuario,'informacion':informacion }
       
    return HttpResponseRedirect(reverse('principalInicio')) 	        
  
   
#Ver Todas la notificaciones Aceptadas
@login_required
def notificaciones_aceptadas(request):
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.    
    usuario = request.user
    albumes = Album.objects.filter(fkusuario=usuario)
    informacion = Notificacion.objects.filter(usuario=usuario)
    contexto = {'albumes': albumes,'usuario': usuario,'informacion':informacion}
    outfile.write('notificaciones_aceptadas -- USER:'+ usuario.username +' NAME:'+ usuario.first_name + ' LASTNAME:' + usuario.last_name + ', NOTIFICACIONES QUE USUARIO A ACEPTADO\n')
    outfile.close()
    return render_to_response('NotificacionesAprobadas.html',context_instance=RequestContext(request,contexto))



#---------------- R E L A C I O N   A M I S T A D ------------------

#Crear Relacion
@login_required
def registro_amigo(request):
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.    
    usuario = request.user    
    if request.method == 'POST':
        formulario = RegistroAmigo(request.POST)
        if formulario.is_valid():
            formulario.procesar_amigo(usuario)
            return HttpResponseRedirect(reverse('principalInicio'))
    formulario = RegistroAmigo()
    contexto = {'usuario': usuario, 'perfil': perfil, 'formulario': formulario}
    outfile.write('registro_amigo -- USER:'+ usuario.username +' NAME:'+ usuario.first_name + ' LASTNAME:' + usuario.last_name + ', SE AGREGARA UN AMIGO NUEVO\n')
    outfile.close()
    return render_to_response('verUsuario.html',context_instance=RequestContext(request,contexto))

#Eliminar amigo
@login_required
def borrarAmigo(request,id_amigo):       
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.    
    usuario = request.user
    usu_amigo = get_object_or_404(User, id=id_amigo)	    
    outfile.write('borrarAmigo -- USER:'+ usuario.username +' NAME:'+ usuario.first_name + ' LASTNAME:' + usuario.last_name + ', SE ELIMINARA A UNO DE SUS AMIGOS\n')    
    usu_logueado = User.objects.get(id=usuario.id)
    usu_logueado.usuarioperfil.amigos.remove(usu_amigo)
    usu_amigo.usuarioperfil.amigos.remove(usu_logueado)
    amigos = UsuarioPerfil.objects.filter(amigos=usuario.id)
    id_per = [amigo.id+1 for amigo in amigos] 
    persona = User.objects.filter(id__in=id_per)    
    outfile.close()
    contexto = {'persona': persona, 'usuario': usuario}
    return render_to_response('verAmigos.html',context_instance=RequestContext(request,contexto))
   
#Ver Amigos 
@login_required
def ver_amigos(request):        
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.    
    usuario = request.user
    outfile.write('ver_amigos -- USER:'+ usuario.username +' NAME:'+ usuario.first_name + ' LASTNAME:' + usuario.last_name + ', SE VERAN TODO SUS AMIGOS\n')
    outfile.close() 
    amigos = UsuarioPerfil.objects.filter(amigos=usuario.id)
    id_per = [amigo.id+1 for amigo in amigos] #lista por comprension
    persona = User.objects.filter(id__in=id_per)
    contexto = {'persona': persona, 'usuario': usuario}
    return render_to_response('verAmigos.html',context_instance=RequestContext(request,contexto))


#Ver Amigos buscados
@login_required
def ver_usuario(request, nombre):
    outfile = open('archivoLogs.txt', 'a') # Indicamos el valor 'w'.
    usuario = request.user  
    outfile.write('ver_usuario -- USER:'+ usuario.username +' NAME:'+ usuario.first_name + ' LASTNAME:' + usuario.last_name + ', SE VEN LOS USUARIOS QUE FUERON OBTENIDOS EN EL BUSCADOR DE AMIGOS\n')
    outfile.close()
             
    if 'buscar' in request.POST:            
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
    usuario = request.user
    outfile.write('ver_PerfilAmigo -- USER:'+ usuario.username +' NAME:'+ usuario.first_name + ' LASTNAME:' + usuario.last_name + ', MOSTRANDO PERLFIL DE LOS AMIGOS\n')
    outfile.close()
    
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



