# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GeoAddress'
        db.create_table(u'geocode_geoaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('uuid', self.gf('uuidfield.fields.UUIDField')(unique=True, max_length=32)),
            ('cluster', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('address', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'geocode', ['GeoAddress'])

        # Adding model 'GeoData'
        db.create_table(u'geocode_geodata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geocode.GeoAddress'])),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'geocode', ['GeoData'])

        # Adding model 'Tag'
        db.create_table(u'geocode_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'geocode', ['Tag'])


    def backwards(self, orm):
        # Deleting model 'GeoAddress'
        db.delete_table(u'geocode_geoaddress')

        # Deleting model 'GeoData'
        db.delete_table(u'geocode_geodata')

        # Deleting model 'Tag'
        db.delete_table(u'geocode_tag')


    models = {
        u'geocode.geoaddress': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'GeoAddress'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'cluster': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32'})
        },
        u'geocode.geodata': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'GeoData'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geocode.GeoAddress']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'geocode.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['geocode']