from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse



#Prueba
def prueba(request):
	return render_to_response('albumRegistrar.html',context_instance=RequestContext(request))

#Modificar usuario
def modificarUsuario(request):
	return render_to_response('usuarioModificar.html',context_instance=RequestContext(request))


#Login Principal
def login_principal(request):
	return render_to_response('login_principal.html',context_instance=RequestContext(request))


#Registrar Usuario
def registroUsuario(request):
	return render_to_response('usuarioRegistrar.html',context_instance=RequestContext(request))


#Pagina de inicio despues de login
def principalInicio(request):
	return render_to_response('principalinicio.html',context_instance=RequestContext(request))


#Crear Album
def registroAlbum(request):
	return render_to_response('albumRegistrar.html',context_instance=RequestContext(request))


#Modificar Album
def modificarAlbum(request):
	return render_to_response('albumModificar.html',context_instance=RequestContext(request))

