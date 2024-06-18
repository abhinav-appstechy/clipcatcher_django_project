from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage ),
    path('fetch-video-thumbnail/', views.get_video_thumbnail_url ),
    path('video-download/', views.video_download ),
]