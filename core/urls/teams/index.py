from django.urls import path, include
from core.views.teams.index import teams_index

urlpatterns = [
    path('', teams_index, name="teams_index"),
]
