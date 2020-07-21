import cloudscraper
import json
import dateparser
from time import sleep
import re

class StoryFireUser:

    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.__s = cloudscraper.create_scraper()

    def get_subscriber_count(self):
        """
        :return: The StoryFire user's subscriber count
        """
        return int(
            self.__s.get(
                'https://bastet.socialblade.com/storyfire/lookup',
                params={
                    'query': self.channel_id
                }
            ).content.decode()
        )

    def live_subscriber_count_generator(self, request_delay=1000):
        """
        :param request_delay: delay between each subscriber yield in milliseconds (defaults to 1000)
        :yield: the StoryFire user's subscriber count in an infinite loop
        """
        while True:
            try:
                yield self.get_subscriber_count()
                sleep(request_delay)
            except ValueError:
                pass


class TwitchUser:
    
    def __init__(self, tag):
        self.__s = cloudscraper.create_scraper()
        response = self.__s.get(f"https://socialblade.com/twitch/user/{tag}/realtime").text
        matches = re.search(r"<p id=\"rawUser\" style=\"display: none;\">(.+)</p>", response)
        self.channel_id = matches.groups(1)[0]
    
    def get_follower_count(self):
        """
        :return: The Twitch user's follower count
        """
        return int(
            self.__s.get(
                'https://bastet.socialblade.com/twitch/lookup',
                params={
                    'query': self.channel_id
                }
            ).content.decode()
        )
    
    def live_follower_count_generator(self, request_delay=1000):
        """
        :param request_delay: delay between each follower yield in milliseconds (defaults to 1000)
        :yield: the Twitch user's follower count in an infinite loop
        """
        while True:
            try:
                yield self.get_follower_count()
                sleep(request_delay)
            except ValueError:
                pass

class TwitterUser:

    def __init__(self, tag):
        self.tag = tag
        self.__s = cloudscraper.create_scraper()

    def get_follower_count(self):
        """
        :return: The twitter user's follower count
        """
        return int(
            self.__s.get(
                'https://bastet.socialblade.com/twitter/lookup',
                params={
                    'query': self.tag
                }
            ).content.decode()
        )

    def live_follower_count_generator(self, request_delay=1000):
        """
        :param request_delay: delay between each follower yield in milliseconds (defaults to 1000)
        :yield: the twitter user's follower count in an infinite loop
        """
        while True:
            try:
                yield self.get_follower_count()
                sleep(request_delay)
            except ValueError:
                pass


class YouTubeVideo:

    def __init__(self, video_id, title, created_at, comments_num, views_num, rating):
        self.video_id = video_id
        self.title = title
        self.created_at = dateparser.parse(created_at).date()
        self.comments_num = int(comments_num)
        self.views_num = int(views_num)
        self.rating = rating


class YouTubeChannel:

    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.__s = cloudscraper.create_scraper()

    @staticmethod
    def __add_videos(videos):
        for video in videos:
            try:
                yield YouTubeVideo(
                    video_id=video['videoId'],
                    title=video['title'],
                    created_at=video['created_at'],
                    comments_num=video['comments'],
                    views_num=video['views'],
                    rating=video['rating']
                )
            except KeyError:
                pass

    def get_latest_videos(self):
        """
        :yield: 50 or less YouTubeVideo objects
        """
        videos = self.__s.post(
            'https://socialblade.com/js/class/youtube-video-recent',
            data={
                'channelid': self.channel_id
            }
        ).content.decode()
        videos = json.loads(videos)
        return YouTubeChannel.__add_videos(videos)

    def get_most_viewed_videos(self):
        """
        :yield: 50 or less YouTubeVideo objects
        """
        videos = self.__s.post(
            'https://socialblade.com/js/class/youtube-video-mostviewed',
            data={
                'channelid': self.channel_id
            }
        ).content.decode()
        videos = json.loads(videos)
        return YouTubeChannel.__add_videos(videos)

    def get_highest_rated_videos(self):
        """
        :yield: 50 or less YouTubeVideo objects
        """
        videos = self.__s.post(
            'https://socialblade.com/js/class/youtube-video-highestrated',
            data={
                'channelid': self.channel_id
            }
        ).content.decode()
        videos = json.loads(videos)
        return YouTubeChannel.__add_videos(videos)

    def get_most_relevant_videos(self):
        """
        :yield: 50 or less YouTubeVideo objects
        """
        videos = self.__s.post(
            'https://socialblade.com/js/class/youtube-video-relevant',
            data={
                'channelid': self.channel_id
            }
        ).content.decode()
        videos = json.loads(videos)
        return YouTubeChannel.__add_videos(videos)

    def get_subscriber_count(self):
        """
        :return: returns the channel's subscriber count (int).
        """
        return int(
            self.__s.get(
                'https://bastet.socialblade.com/youtube/lookup',
                params=
                {
                    'query': self.channel_id
                }
            ).content.decode()
        )

    def live_subscriber_count_generator(self, request_delay=1000):
        """
        :param request_delay: delay between subscriber yield in milliseconds (defaults to 1000)
        :yield: yields the subscriber count of the youtube channel (int) in an infinite loop
        """
        while True:
            try:
                yield self.get_subscriber_count()
                sleep(request_delay / 1000)
            except ValueError:
                pass
