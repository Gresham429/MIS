from django.urls import path
from core.views.devices.index import devices_index


urlpatterns = [
    path('', devices_index, name='devices_index')
]
