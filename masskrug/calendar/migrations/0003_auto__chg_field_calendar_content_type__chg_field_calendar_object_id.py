# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Calendar.content_type'
        db.alter_column(u'calendar_calendar', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True))

        # Changing field 'Calendar.object_id'
        db.alter_column(u'calendar_calendar', 'object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'Calendar.content_type'
        db.alter_column(u'calendar_calendar', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['contenttypes.ContentType']))

        # Changing field 'Calendar.object_id'
        db.alter_column(u'calendar_calendar', 'object_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=None))

    models = {
        u'calendar.agenda': {
            'Meta': {'ordering': "('calendar__name', 'name')", 'object_name': 'Agenda'},
            'calendar': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'agendas'", 'to': u"orm['calendar.Calendar']"}),
            'color': ('colorful.fields.RGBColorField', [], {'max_length': '7'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'calendar.calendar': {
            'Meta': {'object_name': 'Calendar'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['contenttypes.ContentType']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'calendar.event': {
            'Meta': {'object_name': 'Event'},
            'agenda': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': u"orm['calendar.Agenda']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'places': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'events'", 'symmetrical': 'False', 'to': u"orm['calendar.Place']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'calendar.place': {
            'Meta': {'object_name': 'Place'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['calendar']