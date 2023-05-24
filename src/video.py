import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Video:
    """Класс для ютуб-видео"""
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    # API_KEY = 'AIzaSyCQteHpCPaNYLR27mPcVmOXGQHKSimEUFU'
    api_key: str = os.getenv('API_KEY')

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id) -> None:
        """Экземпляр инициализируется video_id. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id  # id видео
        self.title = None
        self.url = None
        self.views_count = None
        self.like_count = None
        try:
            self.video_info = self.youtube.videos().list(id=self.video_id, part='snippet,statistics').execute()
            if self.video_info['items']:
                self.video_title: str = self.video_info['items'][0]['snippet']['title']  # название видео
                self.video_url = self.video_info['items'][0]['snippet']['thumbnails']['default'][
                    'url']  # ссылка на видео
                self.video_number_views: int = self.video_info['items'][0]['statistics'][
                    'viewCount']  # количество просмотров
                self.video_number_like: int = self.video_info['items'][0]['statistics'][
                    'likeCount']  # количество лайков
            else:
                print(f"Видео {self.video_id} не найдено")
        except HttpError as e:
            if e.resp.status == 404:
                print(f"Видео {self.video_id} не найдено")
            else:
                print(f"Ошибка при получении информации о видео {self.video_id}: {e}")

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    """Класс-потомок Video, имеет собственные атрибуты: video_id и playlist_id"""

    def __init__(self, video_id, playlist_id) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return f"{self.video_title}"
