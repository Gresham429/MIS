from django.urls import path
from core.views.teams.index import teams_index

urlpatterns = [
    path('', teams_index, name="teams_index"),
]
