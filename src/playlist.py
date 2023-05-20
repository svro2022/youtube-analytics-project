import os
from datetime import timedelta
from googleapiclient.discovery import build
from src.video import PLVideo


class PlayList:
    """Класс для плейлиста"""
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    # API_KEY = 'AIzaSyCQteHpCPaNYLR27mPcVmOXGQHKSimEUFU'
    api_key: str = os.getenv('API_KEY')

    # создать специальный объект для работы с API
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id) -> None:
        """Экземпляр инициализируется playlist_id. Дальше все данные будут подтягиваться по API."""
        self.playlist_id = playlist_id
        self.playlist_info = self.youtube.playlists().list(part='snippet', id=self.playlist_id).execute()

        self.title = self.playlist_info['items'][0]['snippet']['title']  # название плейлиста
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'  # ссылка на плейлист

        self.videos = self.get_videos()

    def get_videos(self):
        videos = []
        next_page_token = None
        while True:
            playlist_items = self.youtube.playlistItems().list(part='snippet', playlistId=self.playlist_id,
                                                               maxResults=50, pageToken=next_page_token).execute()
            for item in playlist_items['items']:
                video_id = item['snippet']['resourceId']['videoId']
                videos.append(PLVideo(video_id, self.playlist_id))
            next_page_token = playlist_items.get('nextPageToken')
            if not next_page_token:
                break
        return videos

    @property
    def total_duration(self):
        total_time = timedelta()
        for video in self.videos:
            duration = self.youtube.videos().list(part='contentDetails', id=video.video_id).execute()['items'][0][
                'contentDetails']['duration']
            minutes, seconds = map(int, duration[2:].replace('M', ' ').replace('S', '').split())
            duration = timedelta(minutes=minutes, seconds=seconds)
            total_time += duration
        return total_time

    def show_best_video(self):
        best_video_id = None
        max_likes = 0
        for video in self.videos:
            statistics = self.youtube.videos().list(part='statistics', id=video.video_id).execute()['items'][0][
                'statistics']
            likes = int(statistics['likeCount'])
            if likes > max_likes:
                max_likes = likes
                best_video_id = video.video_id
        return f'https://youtu.be/{best_video_id}'

