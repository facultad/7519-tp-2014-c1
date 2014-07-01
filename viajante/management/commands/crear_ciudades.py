# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from django.utils.translation import ugettext as _
import decimal
import random
import time
from viajante.models import Ciudad

class Command(BaseCommand):

  help=_(u'Crea una determinada cantidad de ciudades en forma random')

  option_list = BaseCommand.option_list + (
    make_option('--cantidad', default=10),
    make_option('--prefijo', default=u'GEN-AUTO'),
    )

  def handle(self,*args,**options):
 
    cantidad=options['cantidad']
    prefijo=options['prefijo']
    
    sufijo_inicial = time.time()

    for i in xrange(cantidad):
      descripcion = u'%s/%s'%(prefijo, sufijo_inicial+i*0.01)
      ciudad = Ciudad.objects.create(
        descripcion = descripcion,
        x = decimal.Decimal(random.randrange(1000000))/100,
        y = decimal.Decimal(random.randrange(1000000))/100)

      self.stdout.write(u'Ciudad %s=(%s, %s) creada con éxito\n' % (
        ciudad.descripcion, ciudad.x, ciudad.y))
