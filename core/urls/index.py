from django.urls import path, include

urlpatterns = [
    path("homepage/", include("core.urls.homepage.index")),
    path("teams/", include("core.urls.teams.index")),
    path("devices/", include("core.urls.devices.index")),
]
