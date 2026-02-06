from django.db import models


class VideoAnalysis(models.Model):
    """Модель для хранения результатов анализа видео"""
    
    video_id = models.CharField(max_length=20, unique=True)
    url = models.URLField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    channel_title = models.CharField(max_length=200)
    published_at = models.DateTimeField()
    view_count = models.BigIntegerField(default=0)
    like_count = models.BigIntegerField(default=0)
    comment_count = models.BigIntegerField(default=0)
    tags = models.JSONField(default=list, blank=True)
    hashtags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Анализ видео'
        verbose_name_plural = 'Анализы видео'
    
    def __str__(self):
        return f"{self.title} ({self.video_id})"
