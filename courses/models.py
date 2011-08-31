from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class Semester(models.Model):
    SEMESTER_CHOICES = (
        ('ws', _('winter semester')),
        ('ss', _('summer semester')),
    )
    
    type = models.CharField(max_length=2, choices=SEMESTER_CHOICES)
    year = models.IntegerField(help_text=_("for example: '2011'"))
    current = models.BooleanField()
    class Meta:
        unique_together = [('type','year')]
    
    def __unicode__(self):
        return u'%s %d' % (self.type.upper(), self.year)
    
    # override the save method s.t. it sets all other semester.current to false when saving a semester with current=true
    def save(self, *args, **kwargs):
        super(Semester, self).save(*args, **kwargs)
        if self.current:
            Semester.objects.exclude(id=self.id).update(current=False)


class Course(models.Model):
    name = models.CharField(max_length=100)
    slug=models.SlugField()
    description = models.TextField()
    admins = models.ManyToManyField(User)
    end_of_preference_phase = models.DateField()
    start_of_registration_phase = models.DateField()
    semester = models.ForeignKey(Semester)
    active = models.BooleanField()
    
    @property
    def capacity(self):
        aggregated = Group.objects.filter(course=self).aggregate(course_capacity=Sum('capacity'))
        return aggregated['course_capacity']
    
    @property
    def used_capacity(self):
        groups = Group.objects.filter(course=self)
        used_capacity = 0
        for group in groups:
            used_capacity += group.used_capacity
        return used_capacity
        
    
    def __unicode__(self):
        return self.name


class Group(models.Model):
    RHYTHM_CHOICES = (
        ('da', _('daily')),
        ('we', _('weekly')),
        ('bw', _('bi-weekly')),
        ('mo', _('monthly')),
        ('ot', _('one time')),
        ('ot', _('other')),
    )
    name = models.CharField(max_length=80)
    slug=models.SlugField()
    description = models.TextField()
    capacity = models.IntegerField()
    place = models.CharField(max_length=40)
    first_date = models.DateField()
    last_date = models.DateField()
    rhythm = models.CharField(max_length=2, choices=RHYTHM_CHOICES)
    starting_time = models.TimeField()
    ending_time = models.TimeField()
    course = models.ForeignKey(Course)
    admins = models.ManyToManyField(User, null=True, blank=True)
    
    @property
    def used_capacity(self):
        return Registration.objects.filter(group=self).count()
    
    def __unicode__(self):
        return u'%s, %s' % (self.course, self.name)
           

class Preference(models.Model):
    max_preferences = 5
    PREFERENCE_CHOICES = [(i, str(i)) for i in range(1, max_preferences+1)]
    
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    preference = models.IntegerField(choices=PREFERENCE_CHOICES)
    
    @property
    def group_capacity(self):
        return self.group.capacity
    
    def __unicode__(self):
        return u'%s, %s: %d' % (self.user, self.group, self.preference)


class Registration(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    
    class Meta:
        unique_together = [('user','group')]
    
    def __unicode__(self):
        return u'%s - %s' % (self.user, self.group)


class CourseOfStudies(models.Model):
    class Meta:
        verbose_name_plural = "Courses of Studies"

    course_of_studies = models.CharField(max_length=40)
    
    def __unicode__(self):
        return u'%s' % (self.course_of_studies)