from django.urls import path, re_path
from core.views.api.user_info import get_user_info, update_user_info
from core.views.api.devices_info import get_devices_list, get_devices_info
from core.views.api.team_info import get_teams_info


urlpatterns = [
    path("get_user_info/", get_user_info, name="get_user_info"),
    path("update_user_info/", update_user_info, name="update_user_info"),
    path("get_devices_list/", get_devices_list, name="get_devices_list"),
    re_path(r'^get_device_detail/(?P<device_name>.+?)/(?P<device_model>.+?)/$', get_devices_info, name="get_devices_info"),
    path("get_teams_info/", get_teams_info, name="get_teams_info")
]