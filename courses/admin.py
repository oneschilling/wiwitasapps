from courses.models import Course, Group, Preference, Registration, Semester, CourseOfStudies
from django.contrib import admin

class GroupInline(admin.TabularInline):
    model = Group

class CourseAdmin(admin.ModelAdmin):
    inlines = [
        GroupInline,
    ]
    
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['__unicode__','current']
    list_editable = ['current']

admin.site.register(Course, CourseAdmin)
admin.site.register(Group)
admin.site.register(Preference)
admin.site.register(Registration)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(CourseOfStudies)