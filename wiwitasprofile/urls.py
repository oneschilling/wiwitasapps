"""
URLConf for Django user registration and authentication.

If the default behavior of the registration views is acceptable to
you, simply use a line like this in your root URLConf to set up the
default URLs for registration::

    (r'^accounts/', include('registration.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

But if you'd like to customize the behavior (e.g., by passing extra
arguments to the various views) or split up the URLs, feel free to set
up your own URL patterns for these views instead. If you do, it's a
good idea to use the names ``registration_activate``,
``registration_complete`` and ``registration_register`` for the
various steps of the user-signup process.

"""


from django.conf.urls.defaults import *
from registration.views import register

from wiwitasprofile.forms import WiwiTasRegistrationForm

urlpatterns = patterns('',
                       # this overwrites the registration url from the registration app
                       url(r'^register/$',
                           register,
                           {'form_class': WiwiTasRegistrationForm},
                           name='registration_register'),
                       )