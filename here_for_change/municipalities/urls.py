from django.urls import path
from .views import MunicipalityList, WardDetail, ArticleDetailView

urlpatterns = [
    path("", MunicipalityList.as_view(), name="municipality_list"),
    path("municipalities/<str:municipality_code>/wards/<str:slug>/", WardDetail.as_view(), name="ward_detail"),
    path("map/", ArticleDetailView.as_view(), name="map")
]
