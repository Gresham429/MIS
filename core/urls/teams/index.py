from django.urls import path, include
from core.views.teams.index import index

urlpatterns = [
    path('', index, name="index"),
]
