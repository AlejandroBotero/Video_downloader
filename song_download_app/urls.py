from django.urls import path
from . import views

urlpatterns = [
    path('', views.song_download_view, name='song_download'),
]