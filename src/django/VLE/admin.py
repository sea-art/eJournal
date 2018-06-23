"""
admin.py.

Give admin rights to edit the VLE models.
"""
from django.contrib import admin
from VLE.models import User, Course, Assignment, Journal, Entry, Participation, Role

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Journal)
admin.site.register(Entry)
admin.site.register(Participation)
admin.site.register(Role)
