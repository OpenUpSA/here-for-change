from django.urls import path
from .views import MunicipalityList, MunicipalityDetail, WardList, WardDetail

from . import views


urlpatterns = [
    path("", MunicipalityList.as_view(), name="municipality_list"),
    path("municipalities/<str:municipality_code>/", MunicipalityDetail.as_view(), name="municipality_detail"),
    path("municipalities/<str:municipality_code>/wards/", WardList.as_view(), name="ward_list"),
    path("municipalities/<str:municipality_code>/wards/<str:slug>/", WardDetail.as_view(), name="ward_detail"),
]
