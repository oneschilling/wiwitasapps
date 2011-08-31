from courses.models import Registration, Group
from django.contrib import messages
from django.utils.translation import ugettext as _


class Registrator:
    """
    provides the functionallity to register users to groups
    """
    
    def register_users_for_groups(self, user_group_mapping):
        for user, group in user_group_mapping.iteritems():
            self.register_user_for_group(user, group)
    
    
    def register_user_for_group(self, user, group):
        """
        Returns a tupel with the created or existing Registration object for the course and a flag:
        If the group capacity is full, the user is not registered and None, False is returned
        Flag
        True: object was created
        False: object wasn not created
        """
        
        # check if user is already registered to a group of this course
        existing_registration = Registration.objects.filter(user=user, group__course=group.course)
        if existing_registration:
            return Registration.objects.get(user=user, group=existing_registration[0].group), False
        else:
            if group.used_capacity < group.capacity:
                return Registration.objects.create(user=user, group=group), True
            else:
                return None, False


