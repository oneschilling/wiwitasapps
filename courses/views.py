from django.views.generic import ListView
from courses.models import Course, Group, Semester, Preference
from courses.registration import Registrator
from courses.allocation import preference_administrator
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms.formsets import formset_factory
from django.contrib import messages
from courses.forms import BasePreferenceFormSet


def course_list(request):
    site_headline = _("List of Courses")
    current_semester = Semester.objects.get(current=True)
    courses = Course.objects.filter(semester=current_semester)
    
    return render_to_response('courses/course_list.html', locals(), context_instance=RequestContext(request))

@login_required
def my_course_list(request):
    site_headline = _("My Courses")
    current_semester = Semester.objects.get(current=True)
    courses = Course.objects.filter(group__registration__user=request.user).filter(semester=current_semester)
    
    return render_to_response('courses/course_list.html', locals(), context_instance=RequestContext(request))

@login_required
def course_details(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    course_groups = Group.objects.filter(course=course)
    
    return render_to_response('courses/course_details.html', locals(), context_instance=RequestContext(request))

@login_required
def group_details(request, course_slug, group_slug):
    course = Course.objects.get(slug=course_slug)
    if course:
        group = Group.objects.get(slug=group_slug, course=course)
        if not group:
            messages.add_message(request, messages.ERROR, _("The group does not exist."))
    else:
        messages.add_message(request, messages.ERROR, _("The course does not exist."))
    
    return render_to_response('courses/group_details.html', locals(), context_instance=RequestContext(request))
    
@login_required
def create_preferences(request, course_slug):    
    course = Course.objects.get(slug=course_slug)
    groups = Group.objects.filter(course=course)
    number_of_preferences = min(len(groups), Preference.max_preferences) # the minimum of the group count and the number of allowed preferences in the model
    
    group_choices = [(g.id, g.name) for g in groups]
    
    class PreferenceForm(forms.Form):
        preference = forms.ChoiceField(choices=group_choices, label=_("preference"))
    
    PrefereceFormSet = formset_factory(PreferenceForm, max_num=number_of_preferences, extra=number_of_preferences, formset=BasePreferenceFormSet)
    
    if request.method == 'POST':    # form was submitted
        formset = PrefereceFormSet(request.POST)
        
        if formset.is_valid():
            # create mapping with user, group and preference from POST data
            pref = 1
            user_group_preference_mapping = []
            
            for form in formset:
                pref_group = form.cleaned_data['preference']
                user_group_preference_mapping.append(
                    (request.user, Group.objects.get(id=pref_group), pref)
                )
                pref += 1
            
            #  delete old preferences and save new ones
            Preference.objects.filter(user=request.user,group__course=course).delete()
            preference_administrator.save_user_preferences_for_groups(user_group_preference_mapping)
            messages.add_message(request, messages.SUCCESS, _("Preferences saved."))
        else:
            # notice: the django 'messages framework' is used. so formset errors have to be converted into correct error messages
            for error_message in formset.non_form_errors():
                messages.add_message(request, messages.ERROR, error_message)
    
    else:   # create form
        formset = PrefereceFormSet()
    
    return render_to_response('courses/create_preferences.html', locals(), context_instance=RequestContext(request))



def register_user_to_group(request, course_slug, group_slug):
    if request.method == 'POST':
        registrator = Registrator()
        group = Group.objects.get(slug=request.POST['register_group_slug'])
        registration,created = registrator.register_user_for_group(request.user, group)
        if created:
            messages.add_message(request, messages.SUCCESS, _("You successfully registered to the group."))
        elif registration:
            messages.add_message(request, messages.ERROR, _("You are already registered to this course."))
        else:
            messages.add_message(request, messages.ERROR, _("You cannot register to this group. The Group is full."))
        
        # go back to the view that called the registration
        default_back_url = "courses/group_details.html"
        back_url = request.META.get('HTTP_REFERER', default_back_url)
        if back_url:
            return HttpResponseRedirect(back_url)
        else:
            return HttpResponseRedirect(default_back_url)