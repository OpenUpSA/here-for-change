from django.contrib import admin
from django.urls import include, path

from . import views


urlpatterns = [
    path("", include("here_for_change.municipalities.urls"),),
    path("admin/", admin.site.urls),
]
