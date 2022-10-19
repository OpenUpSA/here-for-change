from django.urls import path,re_path
from .views import MunicipalityList, WardDetail, WardDetailJson

urlpatterns = [
    path("", MunicipalityList.as_view(), name="municipality_list"),
    re_path(r"municipalities/(?P<municipality_code>[a-zA-Z0-9\-]*)/wards/(?P<slug>[a-zA-Z0-9\-]*).json$", WardDetailJson.as_view(), name="ward_detail_json"),
    path("municipalities/<str:municipality_code>/wards/<str:slug>/", WardDetail.as_view(), name="ward_detail"),
]
