from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import (
    Municipality,
    MunicipalityDetail,
    Ward,
    WardDetail)


class MunicipalityAdmin(admin.ModelAdmin):
    model = Municipality
    list_display = ['name', 'municipality_type',
                    'province', 'district', 'municipality_code']
    list_filter = ['name', 'municipality_type', 'province']


class WardAdmin(admin.ModelAdmin):
    model = Ward
    list_display = ['name', 'municipality']
    list_filter = ['name', 'municipality']

class WardDetailAdmin(admin.ModelAdmin):
    model = WardDetail
    list_display = ['ward', 'field_name',
                    'field_type', 'field_value', 'stage']
    list_filter = ['ward', 'field_name', 'field_type', 'stage']

class MunicipalityDetailAdmin(admin.ModelAdmin):
    model = MunicipalityDetail
    list_display = ['municipality', 'field_name',
                    'field_type', 'field_value', 'stage']
    list_filter = ['municipality', 'field_name', 'field_type', 'stage']


admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Ward, WardAdmin)
admin.site.register(WardDetail, WardDetailAdmin)
admin.site.register(MunicipalityDetail, MunicipalityDetailAdmin)
