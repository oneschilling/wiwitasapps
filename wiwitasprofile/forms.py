from django import forms
from registration.forms import RegistrationForm
from courses.models import CourseOfStudies
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from wiwitasprofile.models import WiwiTasProfile
from registration.models import RegistrationProfile



attrs_dict = { 'class': 'required' }


   
class WiwiTasRegistrationForm(RegistrationForm):
    """
    Subclass of ``RegistrationForm`` which ...
    
    """
    
    gender = forms.ChoiceField(choices=WiwiTasProfile.GENDER_CHOICES)
    
    username = forms.CharField(widget=forms.HiddenInput, required=False)
    
    first_name = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                maxlegth=50)),
                                label=_(u'First name'))
    
    last_name = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                maxlegth=50)),
                                label=_(u'Last name'))
    
    matriculation_number = forms.RegexField(regex=r'^108\d{9}$',
                                max_length=12,
                                widget=forms.TextInput(attrs=attrs_dict),
                                initial='108',
                                label=_(u'Matriculation number'))
    
    course_of_studies = forms.ModelChoiceField(queryset=CourseOfStudies.objects.all())
    
    
    def clean_username(self):
        "This function is required to overwrite an inherited username clean"
        return self.cleaned_data['username']
    
    
    allowed_domains = ['rub.de', 'ruhr-uni-bochum.de']
    
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email'].split('@')[0]):
            raise forms.ValidationError(_(u'This email address is already in use. Please supply a different email address.'))
        
        # Check if the supplied email address is a rub address
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain not in self.allowed_domains:
            raise forms.ValidationError(_(u'Registration using non RUB email addresses is prohibited. Please supply a RUB email address.'))
        
        return self.cleaned_data['email']
    
    def clean_matriculation_number(self):
        """
        Validate that the supplied matriculation number is unique for the site.
        
        """
        if WiwiTasProfile.objects.filter(matriculation_number=self.cleaned_data['matriculation_number']):
            raise forms.ValidationError(_(u'This matriculation number is already in use. Please supply a different matriculation number. If this ist in fact your matriculation number and you didn\'t register an account, please contact the support.'))
        
        return self.cleaned_data['matriculation_number']
    
    
    def clean(self):
        if not self.errors:
            #set first part of the email adresse as username
            self.cleaned_data['username'] = '%s' % (self.cleaned_data['email'].split('@',1)[0])
        super(WiwiTasRegistrationForm, self).clean()
        return self.cleaned_data
    
    def save(self, profile_callback=None):
        """
        Create the new ``User`` and ``RegistrationProfile``, and
        returns the ``User``.
        
        This is essentially a light wrapper around
        ``RegistrationProfile.objects.create_inactive_user()``,
        feeding it the form data and a profile callback (see the
        documentation on ``create_inactive_user()`` for details) if
        supplied.
        
        """
        
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
                                                                    password=self.cleaned_data['password1'],
                                                                    email=self.cleaned_data['email'],
                                                                    profile_callback=profile_callback,
                                                                    send_email=False)
        
        wiwitas_profile = WiwiTasProfile.objects.create(user=new_user,
                                                        first_name=self.cleaned_data['first_name'],
                                                        last_name=self.cleaned_data['last_name'],
                                                        gender=self.cleaned_data['gender'],
                                                        matriculation_number=self.cleaned_data['matriculation_number'],
                                                        course_of_studies=self.cleaned_data['course_of_studies'])
        
        return new_user

