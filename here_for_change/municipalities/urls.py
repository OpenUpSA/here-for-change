from django.urls import path
from .views import MunicipalityList, WardDetail

urlpatterns = [
    path("", MunicipalityList.as_view(), name="municipality_list"),
    path("municipalities/<str:municipality_code>/wards/<str:slug>/", WardDetail.as_view(), name="ward_detail"),
]
