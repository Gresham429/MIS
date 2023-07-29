from django.urls import path
from core.views.myspace.index import myspace_index

urlpatterns = [
    path('', myspace_index, name='user_profile')
]
