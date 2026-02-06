from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/', views.analyze_video, name='analyze_video'),
    path('video/<str:video_id>/', views.video_detail, name='video_detail'),
    path('api/video-info/', views.api_video_info, name='api_video_info'),
]
