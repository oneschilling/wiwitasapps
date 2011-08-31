from courses.models import Preference
import random

class PreferenceAdministrator():
    """
    provides the functionallity to create preferences
    """

    def save_user_preferences_for_groups(self, user_group_preference_mapping):
        """
        saves a list of (user, group, preference) tuples
        user and group have to be objects not IDs
        """
        
        for user, group, preference in user_group_preference_mapping:
            self.save_user_preference_for_group(user, group, preference)
    
    def save_user_preference_for_group(self, user, group, preference):
        """
        Returns a tupel with the created or existing Preference object and a flag:
        True: object was created
        False: object already existed
        """
        
        return Preference.objects.get_or_create(user=user, group=group, preference=preference)
    
preference_administrator = PreferenceAdministrator()



class RandomCourseAllocator():
    """
    provides the functionallity to allocate users randomly distributed but with respect to their preferences for one course
    """
    
    def __init__(self, preferences):
        """
        premise: preferences are complete and for exactly ONE course
        first preferences are shuffled and then ordered (stable) by preference
        """
        
        if not type(preferences) == list:
            raise TypeError('preferences must be a list')
        
        self.preferences = preferences
        random.shuffle(self.preferences)
        self.preferences.sort(key=lambda p: -p.preference)  # sort the preferences by preference in DESCENDING order. otherwise preferences.pop() would't return the highest (1) preferences at first
        
        self.registrations = {}
        self.all_users = set([p.user_id for p in self.preferences])
        self.allocations_for_group = {}     # contains the number of users who are allocated to the groups
        self.group_capacities = {}
        for preference in self.preferences:
            self.group_capacities[preference.group_id] = preference.group_capacity
        
        
    def get_group_with_most_free_spaces(self):
        best_group = None
        max_free_spaces = 0
        for group, capacity in self.group_capacities.iteritems():
            free_spaces = capacity - self.allocations_for_group.get(group,0)
            if free_spaces > max_free_spaces:
                best_group = group
                max_free_spaces = free_spaces
        return best_group
        
    
    def get_allocation(self):
        """
        returns a random allocation
        approach to get an allocation
            phase 1: allocate all users to the group with their highest preferene if the group is not full. if the grup is full, try the second, ... preference
            phase 2: all users that have no group will be added successive to the group with the most free spaces
                in this way the groups will be filled evenly
        """
        
        # phase 1
        while self.preferences:
            preference = self.preferences.pop()
            group_allocations = self.allocations_for_group.get(preference.group_id,0)
            if preference.user_id not in self.registrations and group_allocations < preference.group_capacity:
                self.add_user_to_registrations(preference.user_id, preference.group_id, group_allocations)
        
        #phase 2
        unallocated_users = self.all_users - set(self.registrations)
        for user in unallocated_users:
            best_group = self.get_group_with_most_free_spaces()
            if best_group == None:
                raise ValueError("not enough capacity")
            group_allocations = self.allocations_for_group.get(best_group,0)
            self.add_user_to_registrations(user, best_group, group_allocations)
        
        return self.registrations
    
    
    def add_user_to_registrations(self, user, group, group_allocations):
        self.registrations[user] = group
        self.allocations_for_group[group] = group_allocations + 1