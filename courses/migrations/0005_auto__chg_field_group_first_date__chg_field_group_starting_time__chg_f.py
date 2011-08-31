# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Group.first_date'
        db.alter_column('courses_group', 'first_date', self.gf('django.db.models.fields.DateField')(default=datetime.date(2011, 8, 10)))

        # Changing field 'Group.starting_time'
        db.alter_column('courses_group', 'starting_time', self.gf('django.db.models.fields.TimeField')(default=datetime.date(2011, 8, 10)))

        # Changing field 'Group.last_date'
        db.alter_column('courses_group', 'last_date', self.gf('django.db.models.fields.DateField')(default=0))

        # Changing field 'Group.ending_time'
        db.alter_column('courses_group', 'ending_time', self.gf('django.db.models.fields.TimeField')(default=0))


    def backwards(self, orm):
        
        # Changing field 'Group.first_date'
        db.alter_column('courses_group', 'first_date', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Group.starting_time'
        db.alter_column('courses_group', 'starting_time', self.gf('django.db.models.fields.TimeField')(null=True))

        # Changing field 'Group.last_date'
        db.alter_column('courses_group', 'last_date', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Group.ending_time'
        db.alter_column('courses_group', 'ending_time', self.gf('django.db.models.fields.TimeField')(null=True))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'courses.course': {
            'Meta': {'object_name': 'Course'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_of_preference_phase': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Semester']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'start_of_registration_phase': ('django.db.models.fields.DateField', [], {})
        },
        'courses.group': {
            'Meta': {'object_name': 'Group'},
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'null': 'True', 'symmetrical': 'False'}),
            'capacity': ('django.db.models.fields.IntegerField', [], {}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Course']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'ending_time': ('django.db.models.fields.TimeField', [], {}),
            'first_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_date': ('django.db.models.fields.DateField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'rhythm': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'starting_time': ('django.db.models.fields.TimeField', [], {})
        },
        'courses.preference': {
            'Meta': {'object_name': 'Preference'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preference': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'courses.registration': {
            'Meta': {'object_name': 'Registration'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'courses.semester': {
            'Meta': {'unique_together': "[('type', 'year')]", 'object_name': 'Semester'},
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['courses']
