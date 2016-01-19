# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Tag.tag'
        db.alter_column(u'geocode_tag', 'tag', self.gf('django.db.models.fields.CharField')(unique=True, max_length=4096))

        # Changing field 'GeoData.tags'
        db.alter_column(u'geocode_geodata', 'tags', self.gf('django.db.models.fields.CharField')(max_length=4096))

        # Changing field 'GeoAddress.cluster'
        db.alter_column(u'geocode_geoaddress', 'cluster', self.gf('django.db.models.fields.CharField')(max_length=4096, null=True))

    def backwards(self, orm):

        # Changing field 'Tag.tag'
        db.alter_column(u'geocode_tag', 'tag', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True))

        # Changing field 'GeoData.tags'
        db.alter_column(u'geocode_geodata', 'tags', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'GeoAddress.cluster'
        db.alter_column(u'geocode_geoaddress', 'cluster', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

    models = {
        u'geocode.geoaddress': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'GeoAddress'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'cluster': ('django.db.models.fields.CharField', [], {'max_length': '4096', 'null': 'True'}),
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
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '4096'}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'geocode.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4096'})
        }
    }

    complete_apps = ['geocode']