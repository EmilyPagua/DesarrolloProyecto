from django.test import TestCase
from polls.models import UsuarioPerfil, Album ,Notificacion, Contenido, Historial, Contenido, Comentario, Like
from django.contrib.auth.models import User

class PasswordTest(TestCase):
# Crea registros

   def setUp(self):
       self.client = Client()
       self.user = User(username="test", email="test@test.com", first_name="foo", last_name="bar")
       self.user.save()
 
#Prueba la funcionalidad
   def test__password_forgot(self):
       self.assertEquals(PasswordRecovery.objects.count(), 0)

       post_data = {'email': self.user.email}
       response = self.client.post(reverse('password-forgot'), post_data)
       #Evalúa los resultados
       self.assertEquals(response.status_code, 200)
       self.assertEquals(PasswordRecovery.objects.count(), 1)
       self.assertEquals(PasswordRecovery.objects.get(id=1).user, self.user)
       self.assertEquals(len(mail.outbox), 1)
#limpia la base de datos, no es necesario en django
   def setUp(self):
       self.user.delete()      

