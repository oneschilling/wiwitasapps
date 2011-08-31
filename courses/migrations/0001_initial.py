# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Semester'
        db.create_table('courses_semester', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('courses', ['Semester'])

        # Adding model 'Course'
        db.create_table('courses_course', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('end_of_preference_phase', self.gf('django.db.models.fields.DateField')()),
            ('start_of_registration_phase', self.gf('django.db.models.fields.DateField')()),
            ('semester', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Semester'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('courses', ['Course'])

        # Adding M2M table for field admins on 'Course'
        db.create_table('courses_course_admins', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm['courses.course'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('courses_course_admins', ['course_id', 'user_id'])

        # Adding model 'Group'
        db.create_table('courses_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('capacity', self.gf('django.db.models.fields.IntegerField')()),
            ('rhythm', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('place', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Course'])),
        ))
        db.send_create_signal('courses', ['Group'])

        # Adding M2M table for field admins on 'Group'
        db.create_table('courses_group_admins', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm['courses.group'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('courses_group_admins', ['group_id', 'user_id'])

        # Adding model 'Preference'
        db.create_table('courses_preference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Group'])),
            ('preference', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('courses', ['Preference'])

        # Adding model 'Registration'
        db.create_table('courses_registration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Group'])),
        ))
        db.send_create_signal('courses', ['Registration'])


    def backwards(self, orm):
        
        # Deleting model 'Semester'
        db.delete_table('courses_semester')

        # Deleting model 'Course'
        db.delete_table('courses_course')

        # Removing M2M table for field admins on 'Course'
        db.delete_table('courses_course_admins')

        # Deleting model 'Group'
        db.delete_table('courses_group')

        # Removing M2M table for field admins on 'Group'
        db.delete_table('courses_group_admins')

        # Deleting model 'Preference'
        db.delete_table('courses_preference')

        # Deleting model 'Registration'
        db.delete_table('courses_registration')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
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
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_of_preference_phase': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Semester']"}),
            'start_of_registration_phase': ('django.db.models.fields.DateField', [], {})
        },
        'courses.group': {
            'Meta': {'object_name': 'Group'},
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']"}),
            'capacity': ('django.db.models.fields.IntegerField', [], {}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['courses.Course']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'rhythm': ('django.db.models.fields.CharField', [], {'max_length': '2'})
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
            'Meta': {'object_name': 'Semester'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['courses']
