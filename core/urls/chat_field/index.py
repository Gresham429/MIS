from django.urls import path
from core.views.chat_field.index import chat_field_index


urlpatterns = [
    path("", chat_field_index, name="chat_field_index"),
]