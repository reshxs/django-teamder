from django.contrib import admin

from .models import Project, Member, Technology

admin.site.register(Project)
admin.site.register(Member)
admin.site.register(Technology)
