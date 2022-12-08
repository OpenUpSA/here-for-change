from django.urls import path,re_path
from .views import Home, WardDetail, WardDetailJson, FindMyWardCouncillor, RedirectClosestWard, WhoIsMyWardCouncillor, MunicipalityDetailJson, Feedback, UpdateWardDetailFeedback

urlpatterns = [
    path("", Home.as_view(), name="home"),
    re_path(r"municipalities/(?P<municipality_code>[a-zA-Z0-9\-]*)/wards/(?P<slug>[a-zA-Z0-9\-]*).json$", WardDetailJson.as_view(), name="ward_detail_json"),
    path("municipalities/<str:municipality_code>/wards/<str:slug>/", WardDetail.as_view(), name="ward_detail"),
    path("find-my-ward-councillor", FindMyWardCouncillor.as_view(), name="find_councillor"),
    path("to-closest-ward/",RedirectClosestWard.as_view(),name="redirect-to-closest-ward"),
    path("municipalities/<str:municipality_code>/wards/<str:slug>/ward-councillor", WhoIsMyWardCouncillor.as_view(), name="councillor_info"),
    re_path(r"municipalities/(?P<municipality_code>[a-zA-Z0-9\-]*).json$", MunicipalityDetailJson.as_view(), name="municipality_detail_json"),
    path("feedback", Feedback.as_view(), name="feedback"),
    path("update-ward-detail-feedback/<str:ward_slug>/<str:field>/",UpdateWardDetailFeedback.as_view(),name="update_ward_detail_feedback")
]
