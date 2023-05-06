import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    # API_KEY = 'AIzaSyCQteHpCPaNYLR27mPcVmOXGQHKSimEUFU'
    api_key: str = os.getenv('API_KEY')

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id  # id канала
        self.channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title: str = self.channel['items'][0]['snippet']['title']  # название канала
        self.description = self.channel['items'][0]['snippet']['description']  # описание канала
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"  # ссылка на канал
        self.subscriberCount = self.channel['items'][0]['statistics']['subscriberCount']  # количество подписчиков
        self.video_count = self.channel['items'][0]['statistics']['videoCount']  # количество видео
        self.viewCount = self.channel['items'][0]['statistics']['viewCount']  # общее количество просмотров

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """класс-метод `get_service()`, возвращающий объект для работы с YouTube API"""
        return cls.youtube

    def to_json(self, filename):
        """метод `to_json()`, сохраняющий в файл значения атрибутов экземпляра Channel"""

        data = {'channel_id': self.channel_id,
                'channel': self.channel,
                'title': self.title,
                'description': self.description,
                'url': self.url,
                'subscriberCount': self.subscriberCount,
                'video_count': self.video_count,
                'viewCount': self.viewCount}
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
