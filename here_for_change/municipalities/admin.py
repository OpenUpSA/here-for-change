from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import (
    Municipality,
    Ward)


class MunicipalityAdmin(admin.ModelAdmin):
    model = Municipality
    list_display = ['name']
    list_filter = ['name']

class WardAdmin(admin.ModelAdmin):
    model = Ward
    list_display = ['name', 'municipality']
    list_filter = ['name', 'municipality']

admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Ward, WardAdmin)