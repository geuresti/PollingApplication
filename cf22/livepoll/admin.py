from django.contrib import admin
from .models import Poll, Answer

admin.site.site_header = "Livepoll Admin Page"

admin.site.register(Poll)
admin.site.register(Answer)
