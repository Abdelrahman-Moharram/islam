from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'quran'

urlpatterns = [
    path("", index, name='index'),
    path("surah/", get_index_surah, name=""),
    # path("surah/seed/", seed_data, name=""),
    path("surah/<str:id>/", get_surah_by_id, name=""),
]
