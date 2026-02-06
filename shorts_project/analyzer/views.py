from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import VideoAnalysis
from .youtube_service import YouTubeService
from datetime import datetime


def index(request):
    """Главная страница с формой анализа"""
    recent_analyses = VideoAnalysis.objects.all()[:10]
    return render(request, 'analyzer/index.html', {
        'recent_analyses': recent_analyses
    })


@require_http_methods(["POST"])
def analyze_video(request):
    """Анализ видео по URL"""
    url = request.POST.get('video_url', '').strip()
    
    if not url:
        messages.error(request, 'Введите URL видео')
        return redirect('index')
    
    try:
        # Инициализируем сервис YouTube
        youtube_service = YouTubeService()
        
        # Получаем информацию о видео
        video_info = youtube_service.analyze_video_url(url)
        
        # Сохраняем или обновляем в базе данных
        video_analysis, created = VideoAnalysis.objects.update_or_create(
            video_id=video_info['video_id'],
            defaults={
                'url': video_info['url'],
                'title': video_info['title'],
                'description': video_info['description'],
                'channel_title': video_info['channel_title'],
                'published_at': datetime.fromisoformat(video_info['published_at'].replace('Z', '+00:00')),
                'view_count': video_info['view_count'],
                'like_count': video_info['like_count'],
                'comment_count': video_info['comment_count'],
                'tags': video_info['tags'],
                'hashtags': video_info['hashtags'],
            }
        )
        
        if created:
            messages.success(request, f'Видео успешно проанализировано! Найдено {len(video_info["hashtags"])} хештегов и {len(video_info["tags"])} тегов.')
        else:
            messages.info(request, 'Данные видео обновлены.')
        
        return render(request, 'analyzer/result.html', {
            'video': video_analysis,
            'video_info': video_info
        })
        
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('index')
    except Exception as e:
        messages.error(request, f'Произошла ошибка: {str(e)}')
        return redirect('index')


def video_detail(request, video_id):
    """Детальная информация о проанализированном видео"""
    try:
        video = VideoAnalysis.objects.get(video_id=video_id)
        return render(request, 'analyzer/detail.html', {'video': video})
    except VideoAnalysis.DoesNotExist:
        messages.error(request, 'Видео не найдено в базе данных')
        return redirect('index')


@require_http_methods(["GET"])
def api_video_info(request):
    """API endpoint для получения информации о видео (JSON)"""
    url = request.GET.get('url', '').strip()
    
    if not url:
        return JsonResponse({'error': 'URL не указан'}, status=400)
    
    try:
        youtube_service = YouTubeService()
        video_info = youtube_service.analyze_video_url(url)
        
        return JsonResponse({
            'success': True,
            'data': video_info
        })
        
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Ошибка сервера: {str(e)}'}, status=500)
