import cloudscraper
import json
import dateparser
from time import sleep
import re


class FollowerCounter:

    def __init__(self, tag, lookup_url, regex, regex_url=None):
        self.__s = cloudscraper.create_scraper()
        self.lookup_url = lookup_url
        if regex:
            response = self.__s.get(regex_url.replace('{tag}', tag)).text
            matches = re.search(r"<p id=\"rawUser\" style=\"display: none;\">(.+)</p>", response)
            tag = matches.groups(1)[0]
        self.tag = tag

    def get_follower_count(self):
        return int(
            self.__s.get(
                self.lookup_url,
                params={
                    'query': self.tag
                }
            ).content.decode()
        )

    def fail_safe_get_follower_count(self):
        while True:
            try:
                follower_count = self.get_follower_count()
                return follower_count
            except ValueError:
                pass

    def live_follower_counter(self, request_delay=500):
        while True:
            try:
                yield self.get_follower_count()
                sleep(request_delay)
            except ValueError:
                pass


class DailymotionUser(FollowerCounter):
    
    def __init__(self, tag):
        super().__init__(tag, lookup_url='https://bastet.socialblade.com/dailymotion/lookup', regex=True,
                         regex_url="https://socialblade.com/dailymotion/user/{tag}/realtime")

    def initalize(self):
        return super()


class StoryFireUser(FollowerCounter):

    def __init__(self, channel_id):
        super().__init__(tag=channel_id, lookup_url='https://bastet.socialblade.com/storyfire/lookup', regex=False)

    def initalize(self):
        return super()


class TwitchUser(FollowerCounter):
    
    def __init__(self, tag):
        super().__init__(tag, lookup_url='https://bastet.socialblade.com/twitch/lookup', regex=True, regex_url="https://socialblade.com/twitch/user/{tag}/realtime")

    def initalize(self):
        return super()


class TwitterUser(FollowerCounter):

    def __init__(self, tag):
        super().__init__(tag, lookup_url='https://bastet.socialblade.com/twitter/lookup', regex=False)

    def initalize(self):
        return super()


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
            ).content.decode().strip().replace("'", '')
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
