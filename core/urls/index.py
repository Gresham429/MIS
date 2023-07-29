from django.urls import path, include
from core.views.nav.index import sign_in, sign_up, sign_out
from core.views.api.user_info import get_user_info, update_user_info


urlpatterns = [
    path("", include("core.urls.homepage.index")),
    path("signin/", sign_in, name="sign_in"),
    path("signup/", sign_up, name="sign_up"),
    path("signout/", sign_out, name="sign_out"),
    path("teams/", include("core.urls.teams.index")),
    path("devices/", include("core.urls.devices.index")),
    path("<str:username>/", include("core.urls.myspace.index")),
    path("api/get_user_info/", get_user_info, name="get_user_info"),
    path("api/update_user_info/", update_user_info, name="update_user_info"),
]
