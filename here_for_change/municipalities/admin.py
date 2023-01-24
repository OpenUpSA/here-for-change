from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .models import (
    Province,
    Municipality,
    MunicipalityDetail,
    Ward,
    WardDetail,
    FindMyWardCouncillorFeedback)

class ProvinceAdmin(admin.ModelAdmin):
    model = Province
    list_display = ['name','province_code']


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

class FindMyWardCouncillorFeedbackAdmin(admin.ModelAdmin):
    model = FindMyWardCouncillorFeedback
    list_display = ['ward','email','feedback','created_at','updated_at']
    list_filter = ['email','created_at','updated_at','ward']

admin.site.register(Province, ProvinceAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Ward, WardAdmin)
admin.site.register(WardDetail, WardDetailAdmin)
admin.site.register(MunicipalityDetail, MunicipalityDetailAdmin)
admin.site.register(FindMyWardCouncillorFeedback, FindMyWardCouncillorFeedbackAdmin)
