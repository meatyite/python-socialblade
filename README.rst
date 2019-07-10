
Socialblade API wrapper
=======================

Socialblade API wrapper.

Examples
--------

Live YouTube subscriber count
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prints PewDiePie's subscriber count in real time.

.. code-block::

   from socialblade import YouTubeChannel


   pewdiepie_channel = YouTubeChannel('UC-lHJZR3Gqxm24_Vd_AJ5Yw')

   for sub in pewdiepie_channel.live_subscriber_count_generator():
       print(sub)

You could also just get the subscriber count as it is at the time, like this:

.. code-block::

   from socialblade import YouTubeChannel


   pewdiepie_channel = YouTubeChannel('UC-lHJZR3Gqxm24_Vd_AJ5Yw')

   print(pewdiepie_channel.get_subscriber_count())

Export a Channel's Most Viewed Videos Statistics to CSV
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this example we are exporting statistics about PewDiePie's most viewed videos to CSV.

.. code-block::

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

You could do the same thing to any channel. You could also export different types of statistics about videos, which I will list the functions for them here:


* socialblade.YouTubeChannel(channel_id).get_latest_videos()
* socialblade.YouTubeChannel(channel_id).get_most_viewed_videos()
* socialblade.YouTubeChannel(channel_id).get_highest_rated_videos()
* socialblade.YouTubeChannel(channel_id).get_most_relevant_videos()

Get live Twitter follower count
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The twitter functionality is limited in this wrapper to retrieving follower counts.
You could get a twitter users live follower count similer to how you get a youtuber's live follower count:

.. code-block::

   from socialblade import TwitterUser


   donald_trump_twitter = TwitterUser('realdonaldtrump')

   for follower in donald_trump_twitter.live_follower_count_generator(request_delay=500):
       print(follower)

You could also get the follower count as it is at the moment, like so:

.. code-block::

   from socialblade import TwitterUser


   donald_trump_twitter = TwitterUser('realdonaldtrump')

   print(donald_trump_twitter.get_follower_count())
