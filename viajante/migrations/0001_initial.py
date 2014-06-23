# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ciudad'
        db.create_table(u'viajante_ciudad', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('x', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('y', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
        ))
        db.send_create_signal(u'viajante', ['Ciudad'])

        # Adding unique constraint on 'Ciudad', fields ['x', 'y']
        db.create_unique(u'viajante_ciudad', ['x', 'y'])

        # Adding model 'Problema'
        db.create_table(u'viajante_problema', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('max_generations', self.gf('django.db.models.fields.IntegerField')(default=50)),
            ('pop_size', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('distancia_solucion', self.gf('django.db.models.fields.IntegerField')(default=10)),
        ))
        db.send_create_signal(u'viajante', ['Problema'])

        # Adding model 'CiudadProblema'
        db.create_table(u'viajante_ciudadproblema', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('problema', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viajante.Problema'])),
            ('ciudad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viajante.Ciudad'])),
        ))
        db.send_create_signal(u'viajante', ['CiudadProblema'])

        # Adding unique constraint on 'CiudadProblema', fields ['problema', 'ciudad']
        db.create_unique(u'viajante_ciudadproblema', ['problema_id', 'ciudad_id'])

        # Adding model 'ResolucionProblema'
        db.create_table(u'viajante_resolucionproblema', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('orden', self.gf('django.db.models.fields.IntegerField')()),
            ('ciudad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viajante.Ciudad'])),
            ('problema', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['viajante.Problema'])),
        ))
        db.send_create_signal(u'viajante', ['ResolucionProblema'])

        # Adding unique constraint on 'ResolucionProblema', fields ['ciudad', 'problema']
        db.create_unique(u'viajante_resolucionproblema', ['ciudad_id', 'problema_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ResolucionProblema', fields ['ciudad', 'problema']
        db.delete_unique(u'viajante_resolucionproblema', ['ciudad_id', 'problema_id'])

        # Removing unique constraint on 'CiudadProblema', fields ['problema', 'ciudad']
        db.delete_unique(u'viajante_ciudadproblema', ['problema_id', 'ciudad_id'])

        # Removing unique constraint on 'Ciudad', fields ['x', 'y']
        db.delete_unique(u'viajante_ciudad', ['x', 'y'])

        # Deleting model 'Ciudad'
        db.delete_table(u'viajante_ciudad')

        # Deleting model 'Problema'
        db.delete_table(u'viajante_problema')

        # Deleting model 'CiudadProblema'
        db.delete_table(u'viajante_ciudadproblema')

        # Deleting model 'ResolucionProblema'
        db.delete_table(u'viajante_resolucionproblema')


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
            'distancia_solucion': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_generations': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'pop_size': ('django.db.models.fields.IntegerField', [], {'default': '10'})
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