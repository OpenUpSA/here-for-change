from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

urlpatterns = [
    path(
        'robots.txt',
        view=lambda r: HttpResponse(
            "User-agent: *\nAllow: /\n",
            content_type="text/plain")
    ),
    path("", include("here_for_change.municipalities.urls"),),
    path("admin/", admin.site.urls),
]
