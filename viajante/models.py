# coding=utf-8
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from .exceptions import ProblemaSinCiudadesError, ProblemaConUnicaCiudadError
from django.db import transaction
from random import Random
from time import time
import math
import inspyred

class Ciudad(models.Model):

  descripcion = models.CharField(max_length=100, verbose_name=_(u'Descripción'), unique=True)
  x = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_(u'Posición X'))
  y = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_(u'Posición Y'))

  class Meta:
    ordering = ['descripcion']
    verbose_name = _(u"Ciudad")
    verbose_name_plural = _(u"Ciudades")
    unique_together = (('x', 'y'),)

  def __unicode__(self):
    return u'%s' % self.descripcion

  def distancia(self, ciudad):
    return math.sqrt((self.x - ciudad.x)**2 + (self.y - ciudad.y)**2)

class Problema(models.Model):

  descripcion = models.CharField(max_length=100, verbose_name=_(u'Descripción'), unique=True)
  max_generations = models.IntegerField(verbose_name=_(u'Máxima cantidad generaciones'), default=50)
  pop_size = models.IntegerField(verbose_name=_(u'Tamaño de la población'), default=10)
  distancia_solucion = models.IntegerField(verbose_name=_(u'Distancia del recorrido'), default=0,
    help_text=_(u'Distancia del recorrido una vez solucionado el problema, pasando por todas '+
      u'las ciudades y volviendo a la ciudad inicial'))

  def __unicode__(self):
    return u'%s' % self.descripcion

  def get_ciudades(self):
    for cp in self.ciudadproblema_set.all():
      yield cp.ciudad

  def get_pesos_ciudades(self, ciudades):
    cantidad_ciudades = self.ciudadproblema_set.count()
    pesos = [[0 for _ in xrange(cantidad_ciudades)] for _ in xrange(cantidad_ciudades)]
    i = 0
    for ciudad_i in ciudades:
      j = 0
      for ciudad_j in ciudades:
        pesos[i][j] = ciudad_i.distancia(ciudad_j)
        j += 1
      i += 1
    return pesos

  def has_ciudades(self):
    return self.ciudadproblema_set.count() > 0

  def has_unica_ciudad(self):
    return self.ciudadproblema_set.count() == 1

  @transaction.atomic
  def resolver(self):

    if not self.has_ciudades():
      raise ProblemaSinCiudadesError()
    if self.has_unica_ciudad():
      raise ProblemaConUnicaCiudadError()

    ciudades = [ c for c in self.get_ciudades() ]
    pesos = self.get_pesos_ciudades(ciudades)
    problema = inspyred.benchmarks.TSP(pesos)
    rndm = Random()
    rndm.seed(time())
    ac = inspyred.swarm.ACS(
      rndm, problema.components)
    ac.terminator = inspyred.ec.terminators.generation_termination
    final_pop = ac.evolve(
      generator=problema.constructor, 
      evaluator=problema.evaluator, 
      bounder=problema.bounder,
      maximize=problema.maximize, 
      pop_size=self.pop_size, 
      max_generations=self.max_generations)
    
    best = max(ac.archive)
    self.distancia_solucion = 1/best.fitness

    self.resolucionproblema_set.all().delete()

    orden = 0
    for b in best.candidate:
      self.add_proxima_ciudad_en_solucion(orden, ciudades[b.element[0]])
      orden += 1
    self.add_proxima_ciudad_en_solucion(orden,
      ciudades[best.candidate[-1].element[1]])

    self.save()

  def add_proxima_ciudad_en_solucion(self, orden, ciudad):
    resolucion = self.resolucionproblema_set.create(
      ciudad=ciudad, orden=orden)

class CiudadProblema(models.Model):

  problema = models.ForeignKey(Problema, verbose_name=_(u'Problema'))
  ciudad = models.ForeignKey(Ciudad, verbose_name=_(u'Ciudad'))

  class Meta:
    ordering = ['ciudad__descripcion']
    verbose_name = _(u"Ciudad problema")
    verbose_name_plural = _(u"Ciudades problema")
    unique_together = (('problema', 'ciudad'),)

  def get_x(self):
    return self.ciudad.x
  get_x.short_description = ugettext_lazy(u'Posición X')

  def get_y(self):
    return self.ciudad.y
  get_y.short_description = ugettext_lazy(u'Posición Y')

class ResolucionProblema(models.Model):

  orden = models.IntegerField(verbose_name=_(u'Orden'))
  ciudad = models.ForeignKey(Ciudad, verbose_name=_(u'Ciudad'))
  problema = models.ForeignKey(Problema, verbose_name=_(u'Problema'))

  class Meta:
    ordering = ['orden']
    verbose_name = _(u"Resolución")
    verbose_name_plural = _(u"Resolución")
    unique_together = (('ciudad', 'problema'),)

  def distancia_al_siguiente(self):
    resolucion = ResolucionProblema.objects.filter(
      problema=self.problema)
    try:
      rp = resolucion.get(orden=self.orden+1)
    except ResolucionProblema.DoesNotExist:
      rp = resolucion.get(orden=0)
    return round(self.ciudad.distancia(rp.ciudad),2)
  distancia_al_siguiente.short_description = ugettext_lazy(u'Distancia al siguiente')

  def get_x(self):
    return self.ciudad.x
  get_x.short_description = ugettext_lazy(u'Posición X')

  def get_y(self):
    return self.ciudad.y
  get_y.short_description = ugettext_lazy(u'Posición Y')


