from django.contrib import admin
from .models import *

class CiudadAdmin(admin.ModelAdmin):
  list_display=['id','descripcion','x','y']
  search_fields=['descripcion']

class CiudadProblemaInline(admin.TabularInline):
  readonly_fields=['get_x', 'get_y']
  model=CiudadProblema
  extra = 1

class ResolucionProblemaInline(admin.TabularInline):
  readonly_fields=['orden', 'ciudad', 'get_x', 'get_y', 'distancia_al_siguiente']
  model=ResolucionProblema
  extra = 0

class ResolucionProblemaAdmin(admin.ModelAdmin):
  readonly_fields=['id', 'orden', 'ciudad', 'problema']
  model=ResolucionProblema
  list_display=['orden', 'ciudad', 'get_x', 'get_y', 'distancia_al_siguiente']
  list_filter=['problema',]

class ProblemaAdmin(admin.ModelAdmin):
  readonly_fields=['id', 'distancia_solucion', 'tiempo_resolucion']
  model=Problema
  list_display=['id','descripcion',]
  list_display_links = ('id', 'descripcion')
  search_fields=['descripcion']
  inlines=[CiudadProblemaInline, ResolucionProblemaInline]

admin.site.register(Ciudad,CiudadAdmin)
admin.site.register(ResolucionProblema,ResolucionProblemaAdmin)
admin.site.register(Problema,ProblemaAdmin)
