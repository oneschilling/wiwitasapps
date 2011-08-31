from django import forms
from django.forms.formsets import BaseFormSet
from django.utils.translation import ugettext as _
        
class BasePreferenceFormSet(BaseFormSet):
    def clean(self):
        """Checks that each group is only selected once."""
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        preferences = []
        for i in range(0, self.total_form_count()):
            form = self.forms[i]
            preference = form.cleaned_data['preference']
            if preference in preferences:
                raise forms.ValidationError(_("Each group can only be selected once."))
            preferences.append(preference)