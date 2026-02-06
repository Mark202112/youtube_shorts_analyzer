from django.contrib import admin
from .models import VideoAnalysis


@admin.register(VideoAnalysis)
class VideoAnalysisAdmin(admin.ModelAdmin):
    list_display = ('title', 'channel_title', 'view_count', 'like_count', 'published_at', 'created_at')
    list_filter = ('published_at', 'created_at', 'channel_title')
    search_fields = ('title', 'description', 'channel_title', 'video_id')
    readonly_fields = ('video_id', 'url', 'created_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('video_id', 'url', 'title', 'channel_title')
        }),
        ('Контент', {
            'fields': ('description', 'tags', 'hashtags')
        }),
        ('Статистика', {
            'fields': ('view_count', 'like_count', 'comment_count', 'published_at')
        }),
        ('Служебное', {
            'fields': ('created_at',)
        }),
    )
