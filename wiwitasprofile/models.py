from django.db import models
from django.contrib.auth.models import User
from courses.models import CourseOfStudies
from django.utils.translation import ugettext as _

class WiwiTasProfile(models.Model):
    GENDER_CHOICES = (
        ('m', _('male')),
        ('f', _('female')),
    )
    
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    matriculation_number = models.CharField(max_length=12, unique=True)
    course_of_studies = models.ForeignKey(CourseOfStudies)
    
    def __unicode__(self):
        return u"%s %s (%s)" % (self.first_name, self.last_name, self.matriculation_number)