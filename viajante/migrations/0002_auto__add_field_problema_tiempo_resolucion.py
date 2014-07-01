# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Problema.tiempo_resolucion'
        db.add_column(u'viajante_problema', 'tiempo_resolucion',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=7, decimal_places=3),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Problema.tiempo_resolucion'
        db.delete_column(u'viajante_problema', 'tiempo_resolucion')


    models = {
        u'viajante.ciudad': {
            'Meta': {'ordering': "['descripcion']", 'unique_together': "(('x', 'y'),)", 'object_name': 'Ciudad'},
            'descripcion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'x': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'y': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'})
        },
        u'viajante.ciudadproblema': {
            'Meta': {'ordering': "['ciudad__descripcion']", 'unique_together': "(('problema', 'ciudad'),)", 'object_name': 'CiudadProblema'},
            'ciudad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viajante.Ciudad']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'problema': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viajante.Problema']"})
        },
        u'viajante.problema': {
            'Meta': {'object_name': 'Problema'},
            'descripcion': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'distancia_solucion': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_generations': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'pop_size': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'tiempo_resolucion': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '7', 'decimal_places': '3'})
        },
        u'viajante.resolucionproblema': {
            'Meta': {'ordering': "['orden']", 'unique_together': "(('ciudad', 'problema'),)", 'object_name': 'ResolucionProblema'},
            'ciudad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viajante.Ciudad']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orden': ('django.db.models.fields.IntegerField', [], {}),
            'problema': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['viajante.Problema']"})
        }
    }

    complete_apps = ['viajante']