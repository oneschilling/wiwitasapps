from django.conf.urls.defaults import *

urlpatterns = patterns('courses.views',
    url(r'^$', 'course_list'),
    url(r'^my/$', 'my_course_list'),
    url(r'^(?P<course_slug>\w+)/$', 'course_details'),
    url(r'^(?P<course_slug>\w+)/preferences/$', 'create_preferences'),
    url(r'^(?P<course_slug>\w+)/(?P<group_slug>\w+)/$', 'group_details'),
    url(r'^(?P<course_slug>\w+)/(?P<group_slug>\w+)/register$', 'register_user_to_group'),
)