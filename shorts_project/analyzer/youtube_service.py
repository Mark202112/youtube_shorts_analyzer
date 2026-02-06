"""
Сервис для работы с YouTube Data API v3
"""
import re
from typing import Dict, List, Optional
from django.conf import settings
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class YouTubeService:
    """Класс для работы с YouTube API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.YOUTUBE_API_KEY
        if not self.api_key:
            raise ValueError("YouTube API ключ не установлен. Установите YOUTUBE_API_KEY в настройках.")
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Извлекает video ID из различных форматов YouTube ссылок
        
        Поддерживаемые форматы:
        - https://youtube.com/shorts/VIDEO_ID
        - https://www.youtube.com/shorts/VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://m.youtube.com/watch?v=VIDEO_ID
        """
        patterns = [
            r'(?:youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',
            r'(?:youtu\.be\/)([a-zA-Z0-9_-]{11})',
            r'(?:youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})',
            r'(?:m\.youtube\.com\/watch\?v=)([a-zA-Z0-9_-]{11})',
            r'^([a-zA-Z0-9_-]{11})$'  # Просто ID
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    @staticmethod
    def extract_hashtags(text: str) -> List[str]:
        """
        Извлекает хештеги из текста
        Находит все слова, начинающиеся с #
        """
        if not text:
            return []
        
        # Паттерн для хештегов (поддержка кириллицы и латиницы)
        hashtag_pattern = r'#([a-zA-Zа-яА-ЯёЁїЇіІєЄґҐ0-9_]+)'
        hashtags = re.findall(hashtag_pattern, text)
        
        # Возвращаем уникальные хештеги
        return list(set(hashtags))
    
    def get_video_info(self, video_id: str) -> Dict:
        """
        Получает информацию о видео по ID
        
        Returns:
            Dict с информацией о видео
        """
        try:
            request = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=video_id
            )
            response = request.execute()
            
            if not response.get('items'):
                raise ValueError(f"Видео с ID {video_id} не найдено")
            
            video = response['items'][0]
            snippet = video['snippet']
            statistics = video.get('statistics', {})
            
            # Извлекаем хештеги из описания и названия
            description = snippet.get('description', '')
            title = snippet.get('title', '')
            hashtags = self.extract_hashtags(description + ' ' + title)
            
            # Получаем теги (если есть)
            tags = snippet.get('tags', [])
            
            return {
                'video_id': video_id,
                'title': title,
                'description': description,
                'channel_title': snippet.get('channelTitle', ''),
                'channel_id': snippet.get('channelId', ''),
                'published_at': snippet.get('publishedAt', ''),
                'thumbnail_url': snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                'view_count': int(statistics.get('viewCount', 0)),
                'like_count': int(statistics.get('likeCount', 0)),
                'comment_count': int(statistics.get('commentCount', 0)),
                'tags': tags,
                'hashtags': hashtags,
                'duration': video.get('contentDetails', {}).get('duration', ''),
            }
            
        except HttpError as e:
            if e.resp.status == 403:
                raise ValueError("Ошибка API: проверьте ваш API ключ или квоту")
            elif e.resp.status == 404:
                raise ValueError("Видео не найдено")
            else:
                raise ValueError(f"Ошибка YouTube API: {str(e)}")
        except Exception as e:
            raise ValueError(f"Ошибка при получении данных: {str(e)}")
    
    def analyze_video_url(self, url: str) -> Dict:
        """
        Анализирует видео по URL
        
        Args:
            url: URL YouTube видео или Shorts
            
        Returns:
            Dict с полной информацией о видео
        """
        video_id = self.extract_video_id(url)
        
        if not video_id:
            raise ValueError("Не удалось извлечь ID видео из URL. Проверьте формат ссылки.")
        
        video_info = self.get_video_info(video_id)
        video_info['url'] = url
        
        return video_info
