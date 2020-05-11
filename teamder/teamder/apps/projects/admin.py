from django.contrib import admin

from .models import Project, Member, Ad, Technology

admin.site.register(Project)
admin.site.register(Member)
admin.site.register(Ad)
admin.site.register(Technology)
