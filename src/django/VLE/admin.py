from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Journal)
admin.site.register(Entry)
