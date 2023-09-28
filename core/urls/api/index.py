from django.urls import path, re_path
from core.views.api.user_info import get_user_info, update_user_info
from core.views.api.devices_info import get_devices_list, get_devices_info
from core.views.api.team_info import get_teams_info, getPopUpContent, add_team, update_team, delete_team, get_oneteam_info, get_team_members
from core.views.api.user_info import verify_email
from core.views.api.teammember_info import add_team_member, delete_team_member, getMemberInfo


urlpatterns = [
    path("get_user_info/", get_user_info, name="get_user_info"),
    path("update_user_info/", update_user_info, name="update_user_info"),
    path("get_devices_list/", get_devices_list, name="get_devices_list"),
    re_path(r'^get_device_detail/(?P<device_name>.+?)/(?P<device_model>.+?)/$', get_devices_info, name="get_devices_info"),
    path("<int:team_id>/getPopUpContent/", getPopUpContent, name="getPopUpContent"),
    path("<int:team_id>/get_oneteam_info/", get_oneteam_info, name="get_oneteam_info"),
    path("get_teams_info/", get_teams_info, name="get_teams_info"),
    path("add_team/", add_team, name="add_team"),
    path("<int:member_id>/getMemberInfo/", getMemberInfo, name="getMemberInfo"),
    path("<int:member_id>/delete_team_member/", delete_team_member, name="delete_team_member"),
    path("<int:team_id>/update_team/", update_team, name="update_team"),
    path("<int:team_id>/delete_team/", delete_team, name="delete_team"),
    path("<int:team_id>/get_team_members/", get_team_members, name="get_team_members"),
    path("add_team_member/", add_team_member, name="add_team_member"),
    path("verify_email/", verify_email, name="verify_email")
]