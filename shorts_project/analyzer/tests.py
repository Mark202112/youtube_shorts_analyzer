from django.test import TestCase, Client
from django.urls import reverse
from .youtube_service import YouTubeService


class YouTubeServiceTests(TestCase):
    """Тесты для YouTube Service"""
    
    def test_extract_video_id_shorts(self):
        """Тест извлечения ID из Shorts URL"""
        urls = [
            'https://youtube.com/shorts/ABC123DEF45',
            'https://www.youtube.com/shorts/ABC123DEF45',
            'https://m.youtube.com/shorts/ABC123DEF45',
        ]
        for url in urls:
            video_id = YouTubeService.extract_video_id(url)
            self.assertEqual(video_id, 'ABC123DEF45')
    
    def test_extract_video_id_regular(self):
        """Тест извлечения ID из обычного URL"""
        urls = [
            'https://www.youtube.com/watch?v=ABC123DEF45',
            'https://youtube.com/watch?v=ABC123DEF45',
            'https://m.youtube.com/watch?v=ABC123DEF45',
            'https://youtu.be/ABC123DEF45',
        ]
        for url in urls:
            video_id = YouTubeService.extract_video_id(url)
            self.assertEqual(video_id, 'ABC123DEF45')
    
    def test_extract_video_id_plain(self):
        """Тест извлечения ID из просто ID"""
        video_id = YouTubeService.extract_video_id('ABC123DEF45')
        self.assertEqual(video_id, 'ABC123DEF45')
    
    def test_extract_hashtags(self):
        """Тест извлечения хештегов"""
        text = "Проверка #тест1 и #тест2, также #test3 #123"
        hashtags = YouTubeService.extract_hashtags(text)
        self.assertIn('тест1', hashtags)
        self.assertIn('тест2', hashtags)
        self.assertIn('test3', hashtags)
        self.assertIn('123', hashtags)
    
    def test_extract_hashtags_empty(self):
        """Тест на пустой текст"""
        hashtags = YouTubeService.extract_hashtags("")
        self.assertEqual(hashtags, [])
        
        hashtags = YouTubeService.extract_hashtags(None)
        self.assertEqual(hashtags, [])


class ViewsTests(TestCase):
    """Тесты для представлений"""
    
    def setUp(self):
        self.client = Client()
    
    def test_index_page(self):
        """Тест главной страницы"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'YouTube Shorts Analyzer')
    
    def test_analyze_empty_url(self):
        """Тест с пустым URL"""
        response = self.client.post(reverse('analyze_video'), {'video_url': ''})
        self.assertEqual(response.status_code, 302)  # Redirect
