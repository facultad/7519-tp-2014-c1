from django.contrib import admin
from .models import *

class CiudadAdmin(admin.ModelAdmin):
  list_display=['id','descripcion','x','y']
  search_fields=['descripcion']

class CiudadProblemaInline(admin.TabularInline):
  model=CiudadProblema
  extra = 1

class ResolucionProblemaAdmin(admin.ModelAdmin):
  readonly_fields=['id', 'orden', 'ciudad', 'problema']
  model=ResolucionProblema
  list_display=['orden','ciudad',]
  list_filter=['problema',]

class ProblemaAdmin(admin.ModelAdmin):
  readonly_fields=['id', 'distancia_solucion']
  model=Problema
  list_display=['id','descripcion',]
  search_fields=['descripcion']
  inlines=[CiudadProblemaInline, ]

admin.site.register(Ciudad,CiudadAdmin)
admin.site.register(ResolucionProblema,ResolucionProblemaAdmin)
admin.site.register(Problema,ProblemaAdmin)
