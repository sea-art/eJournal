"""
admin.py.

Give admin rights to edit the VLE models. This is mostly used for editing
inside the web interface through http://site/admin/VLE/user/
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
