from Utils.csv_saver import csv_saver
from Utils.file_name_corrector import sanitize_filename
from Utils.logger import logger
from YoutubeScraper import YouTubeScraper
from constants import api_key

report1 = []
report2 = []

# channel name sample :techTFQ

if __name__ == '__main__':

    channel_name = input("Enter Channel Name:\n")
    scraper = YouTubeScraper(api_key, channel_name)

    playlists = scraper.playlists_extractor()

    for playlist in playlists['items']:
        playlist_id = playlist['id']
        playlist_title = playlist['snippet']['title']
        thumbnail_url = playlist['snippet']['thumbnails']['default']['url']
        pub_date = playlist['snippet']['publishedAt']

        logger.info(f"Playlist: {playlist_title}")
        logger.info(f"Playlist ID: {playlist_id}")
        logger.info(f"Published Date: {pub_date}")
        logger.info(f"Thumbnail: {thumbnail_url}")

        playlist_items = scraper.playlist_items_extractor(playlist_id)

        # Iterate over each video in the playlist
        for item in playlist_items['items']:
            logger.info("*****************************")
            logger.info(f"Video Number:{playlist_items['items'].index(item) + 1}")
            logger.info("*****************************")

            video_id = item['snippet']['resourceId']['videoId']
            video_title = item['snippet']['title']
            video_link = 'https://www.youtube.com/watch?v=' + video_id
            logger.info(f"Video Title: {video_title}")
            logger.info(f"Video ID: {video_id}")
            logger.info(f"Video Link: {video_link}")

            video_response = scraper.video_statistics_extractor(video_id)

            statistics = video_response['items'][0]['statistics']
            view_count = statistics['viewCount']
            like_count = statistics.get('likeCount', 0)
            comment_count = statistics.get('commentCount', 0)

            logger.info(f"Views: {view_count}")
            logger.info(f"Likes: {like_count}")
            logger.info(f"Comments: {comment_count}")

            dic_temp_1 = {'Playlist': playlist_title,
                          'Video title': video_title,
                          'Video ID': video_id,
                          'Video Link': video_link,
                          'Views': view_count,
                          'Likes': like_count,
                          'Comments': comment_count}

            report1.append(dic_temp_1)

            all_comments = scraper.all_comments_extractor(video_id)

            logger.info(len(all_comments))
            for comment in all_comments:
                logger.info(f"Author: {comment['author_name']}")
                logger.info(f"ID: {comment['author_id']}")
                logger.info(f"Text: {comment['comment_text']}")
                logger.info(f"Replies: {comment['replies_count']}")
                logger.info(f"Date: {comment['date']}")

                dic_temp_2 = {
                    'Video title': video_title,
                    'Author': comment['author_name'],
                    'Text': comment['comment_text'],
                    'Replies': comment['replies_count'],
                    'Date': comment['date'],
                }

                report2.append(dic_temp_2)

        logger.info("*****************************")

        # save file
        csv_saver(report2, f'{scraper.files_dir}{sanitize_filename(playlist_title)}.csv')
        report2 = []

    csv_saver(report1, f'{scraper.files_dir}Report1.csv')
