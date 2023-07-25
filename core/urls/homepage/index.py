from django.urls import path, include
from core.views.homepage.index import homepage_index

urlpatterns = [
    path('', homepage_index, name='homepage_index'),
]
