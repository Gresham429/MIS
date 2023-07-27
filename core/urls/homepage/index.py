from django.urls import path
from core.views.homepage.index import homepage_index

urlpatterns = [
    path('', homepage_index, name='homepage_index'),
]
