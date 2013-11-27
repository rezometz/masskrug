# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Place'
        db.create_table(u'calendar_place', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'calendar', ['Place'])

        # Adding model 'Calendar'
        db.create_table(u'calendar_calendar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'calendar', ['Calendar'])

        # Adding model 'Agenda'
        db.create_table(u'calendar_agenda', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('calendar', self.gf('django.db.models.fields.related.ForeignKey')(related_name='agendas', to=orm['calendar.Calendar'])),
            ('color', self.gf('colorful.fields.RGBColorField')(max_length=7)),
        ))
        db.send_create_signal(u'calendar', ['Agenda'])

        # Adding model 'Event'
        db.create_table(u'calendar_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('agenda', self.gf('django.db.models.fields.related.ForeignKey')(related_name='events', to=orm['calendar.Agenda'])),
        ))
        db.send_create_signal(u'calendar', ['Event'])

        # Adding M2M table for field places on 'Event'
        m2m_table_name = db.shorten_name(u'calendar_event_places')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'calendar.event'], null=False)),
            ('place', models.ForeignKey(orm[u'calendar.place'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'place_id'])


    def backwards(self, orm):
        # Deleting model 'Place'
        db.delete_table(u'calendar_place')

        # Deleting model 'Calendar'
        db.delete_table(u'calendar_calendar')

        # Deleting model 'Agenda'
        db.delete_table(u'calendar_agenda')

        # Deleting model 'Event'
        db.delete_table(u'calendar_event')

        # Removing M2M table for field places on 'Event'
        db.delete_table(db.shorten_name(u'calendar_event_places'))


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
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
        }
    }

    complete_apps = ['calendar']