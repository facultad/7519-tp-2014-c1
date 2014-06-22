from django.test import TestCase
from .models import *

# Create your tests here.
class ViajanteTestCase(TestCase):
  
  def test_resolver(self):

    problema = Problema.objects.create(descripcion='Problema de prueba')

    self.assertRaises(ProblemaSinCiudadesError,problema.resolver)


    ciudad = Ciudad.objects.create(descripcion='Ciudad 1',x=0,y=0)
    problema.ciudadproblema_set.create(ciudad=ciudad)

    self.assertRaises(ProblemaConUnicaCiudadError,problema.resolver)


    ciudad = Ciudad.objects.create(descripcion='Ciudad 2',x=4,y=3)
    problema.ciudadproblema_set.create(ciudad=ciudad)

    problema.resolver()

    self.assertEqual(10,problema.distancia_solucion)


    ciudad = Ciudad.objects.create(descripcion='Ciudad 3',x=8,y=0)
    problema.ciudadproblema_set.create(ciudad=ciudad)

    problema.resolver()

    self.assertEqual(18,problema.distancia_solucion)


    ciudad = Ciudad.objects.create(descripcion='Ciudad 4',x=4,y=-3)
    problema.ciudadproblema_set.create(ciudad=ciudad)

    problema.resolver()

    self.assertEqual(20,problema.distancia_solucion)


    ciudad = Ciudad.objects.create(descripcion='Ciudad 5',x=2,y=1.5)
    problema.ciudadproblema_set.create(ciudad=ciudad)

    problema.resolver()

    self.assertEqual(20,problema.distancia_solucion)
