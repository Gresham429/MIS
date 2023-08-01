from django.urls import path, include
from core.views.nav.index import sign_in, sign_up, sign_out


urlpatterns = [
    path("", include("core.urls.homepage.index")),
    path("signin/", sign_in, name="sign_in"),
    path("signup/", sign_up, name="sign_up"),
    path("signout/", sign_out, name="sign_out"),
    path("teams/", include("core.urls.teams.index")),
    path("devices/", include("core.urls.devices.index")),
    path("myspace/", include("core.urls.myspace.index")),
    path("chat_field/", include("core.urls.chat_field.index")),
    path("api/", include("core.urls.api.index"))
]
