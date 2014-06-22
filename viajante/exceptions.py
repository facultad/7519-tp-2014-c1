# coding=utf-8
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError

class ProblemaSinCiudadesError(ValidationError):
  
  def __init__(self):
    ValidationError.__init__(self,
      _(u"El problema no tiene registrada ninguna ciudad."))

class ProblemaConUnicaCiudadError(ValidationError):
  
  def __init__(self):
    ValidationError.__init__(self,
      _(u"El problema debe tener más de una ciudad."))
