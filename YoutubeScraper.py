from googleapiclient.discovery import build

from Utils.directory_creator import directory_creator
from Utils.logger import logger


class YouTubeScraper:
    def __init__(self, api_token, channel_name):
        self.API_KEY = api_token
        self.service = build('youtube', 'v3', developerKey=self.API_KEY)
        self.channel_id = self.channel_id_extractor(channel_name)
        self.channel_link = 'https://www.youtube.com/@' + channel_name
        self.files_dir = directory_creator('csv_files/')

    def channel_id_extractor(self, channelName: str) -> str:
        """extract channel_id by its name"""
        try:
            search_response = self.service.search().list(q=channelName,
                                                         part='id',
                                                         type='channel',
                                                         maxResults=1).execute()
            channel_id = search_response['items'][0]['id']['channelId']
            logger.info(f'Channel Name:{channelName}')
            logger.info(f'Channel ID:{channel_id}')
            logger.info(f"*****************************")

        except Exception as e:
            channel_id = None
            logger.error('Channel ID Not Found.')
        return channel_id

    def playlists_extractor(self):
        """Retrieve playlists from the channel"""
        playlists = self.service.playlists().list(part='snippet',
                                                  channelId=self.channel_id,
                                                  maxResults=50).execute()
        return playlists

    def playlist_items_extractor(self, playlistId: str) -> list:
        """Retrieve playlist items (videos) from each playlist"""
        list_items = self.service.playlistItems().list(part='snippet',
                                                       playlistId=playlistId,
                                                       maxResults=50).execute()
        return list_items

    def video_statistics_extractor(self, videoId):
        video_response = self.service.videos().list(part='statistics', id=videoId).execute()
        return video_response

    def all_comments_extractor(self, videoId):
        comments = []
        nextPageToken = None

        while True:
            response = self.service.commentThreads().list(part='snippet',
                                                          videoId=videoId,
                                                          maxResults=100,  # Maximum number of comments per page
                                                          pageToken=nextPageToken if nextPageToken else ''
                                                          ).execute()

            for comment in response['items']:
                author_name = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
                author_id = comment['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
                comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                replies_count = comment['snippet']['totalReplyCount']
                date = comment['snippet']['topLevelComment']['snippet']['publishedAt']

                comments.append({
                    'author_name': author_name,
                    'author_id': author_id,
                    'comment_text': comment_text,
                    'replies_count': replies_count,
                    'date': date
                })

            nextPageToken = response.get('nextPageToken')

            if not nextPageToken:
                break

        return comments
