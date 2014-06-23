# coding=utf-8
from django.shortcuts import render, redirect
from .models import Problema
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.views.generic import View

class ExecuteMethodView(View):
  _class = None
  method = None

  def get(self, request, *args, **kwargs):
    instance = self._class.objects.get(pk=self.kwargs['pk'])
    try:
      self.method(instance)
      messages.success(request, _(u'Operación realizada en forma exitosa.'))
    except ValidationError as e:
      messages.error(request, e)
    return self.redirect(instance)
  
  def redirect(self, instance):
    raise Exception(_(u'Método no implementado.'))

class ExecuteProblemaMethodView(ExecuteMethodView):
  _class = Problema

  def redirect(self, instance):
    return redirect('/admin/viajante/problema/%s/' % instance.id)


