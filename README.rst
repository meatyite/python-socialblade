Socialblade API wrapper
=======================

| Socialblade API wrapper.
| ***Added Twitch and StoryFire support***

Examples
--------

Live YouTube subscriber count
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Prints PewDiePie's subscriber count in real time.

.. code:: python

    from socialblade import YouTubeChannel


    pewdiepie_channel = YouTubeChannel('UC-lHJZR3Gqxm24_Vd_AJ5Yw')

    for sub in pewdiepie_channel.live_subscriber_count_generator():
        print(sub)

You could also just get the subscriber count as it is at the time, like
this:

.. code:: python

    from socialblade import YouTubeChannel


    pewdiepie_channel = YouTubeChannel('UC-lHJZR3Gqxm24_Vd_AJ5Yw')

    print(pewdiepie_channel.get_subscriber_count())

Export a Channel's Most Viewed Videos Statistics to CSV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this example we are exporting statistics about PewDiePie's most
viewed videos to CSV.

.. code:: python

    from socialblade import YouTubeChannel
    import csv
    from datetime import datetime
    import locale


    locale.setlocale(locale.LC_ALL, '')


    def create_more_readable_ints(integer):
        return locale.currency(integer, symbol=False, grouping=True).replace('.00', '').replace(',', "'")


    pewdiepie_channel = YouTubeChannel('UC-lHJZR3Gqxm24_Vd_AJ5Yw')

    writer = csv.writer(
        open(
            'PewDiePie Most Viewed Videos {}.csv'.format(str(datetime.now().date())),
            'w',
            newline='',
            encoding='utf-8'
        )
    )
    writer.writerow(
        ['Channel', 'Title', 'Created at', 'Views', 'Comments']
    )
    for video in pewdiepie_channel.get_most_viewed_videos():
        writer.writerow(
            [
                'PewDiePie',
                video.title,
                str(video.created_at),
                create_more_readable_ints(video.views_num),
                create_more_readable_ints(video.comments_num)
            ]
        )

You could do the same thing to any channel. You could also export
different types of statistics about videos, which I will list the
functions for them here:

-  socialblade.YouTubeChannel(channel\_id).get\_latest\_videos()
-  socialblade.YouTubeChannel(channel\_id).get\_most\_viewed\_videos()
-  socialblade.YouTubeChannel(channel\_id).get\_highest\_rated\_videos()
-  socialblade.YouTubeChannel(channel\_id).get\_most\_relevant\_videos()

Get live Twitter follower count
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| The Twitter functionality is limited in this wrapper to retrieving
follower counts.
| You could get a Twitter user's live follower count similer to how you
get a youtuber's live follower count:

.. code:: python

    from socialblade import TwitterUser


    donald_trump_twitter = TwitterUser('realdonaldtrump').initalize()

    for follower in donald_trump_twitter.live_follower_counter(request_delay=500):
        print(follower)

You could also get the follower count as it is at the moment, like so:

::

    from socialblade import TwitterUser


    donald_trump_twitter = TwitterUser('realdonaldtrump').initalize()

    print(donald_trump_twitter.get_follower_count())

Get live Twitch and StoryFire follower counts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| Like Twitter, Twitch and StoryFire functionality is also limited to
retrieving follower counts.
| You could compare the follower counts of a user's multiple platforms,
whether that be Twitch and Twitter...:
| *WARNING: Twitch, Dailymotion and StoryFire may or may not work. We
are still working on this issue*

.. code:: python

    from socialblade import TwitterUser, TwitchUser


    user = 'michaelreeves'

    reeves_twitter = TwitterUser(user).initalize()
    reeves_twitch = TwitchUser(user).initalize()

    twitter_followers = reeves_twitter.get_follower_count()
    twitch_followers = reeves_twitch.get_follower_count()

    if twitter_followers > twitch_followers:
        print(f"{user} has {twitter_followers - twitch_followers} more followers on Twitch than on Twitter.")
    else:
        print(f"{user} has {twitch_followers - twitter_followers} more followers on Twitter than on Twitch.")

...or StoryFire and YouTube:

.. code:: python

    from socialblade import YouTubeChannel, StoryFireUser


    rgt_youtube = YouTubeChannel('UCA5RGaQc-a8tIX_AqTTmWdw').initalize()
    rgt_storyfire = StoryFireUser('1fozx1kcs0tuj3').initalize()

    for sf_subscribers in rgt_storyfire.live_follower_counter():
        for yt_subscribers in rgt_youtube.live_subscriber_count_generator():
            print(f"{yt_subscribers} on YouTube vs {sf_subscribers} on StoryFire.")

Get live Dailymotion follower counts.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from socialblade import DailymotionUser


    newsy = DailymotionUser('newsy').initalize()
    print(newsy.get_follower_count())

    for follower in newsy.live_follower_counter(request_delay=500):
        print(follower)

