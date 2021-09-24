#!/usr/bin/env python
# tweepy-bots/bots/autoreply.py

import tweepy
import logging
from config import create_api
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id:
            original_tweet = api.get_status(tweet.in_reply_to_status_id)
            sn = tweet.user.screen_name
            m = "@%s Hello!" % (sn)
            print (m)
            if 'media' in original_tweet.entities:
                media_details = original_tweet.entities['media']
                media_details_kind = media_details[0]
                if media_details_kind['type'] == 'photo' or media_details_kind['type'] == 'animated_gif':
                    try:
                        video_url = media_details_kind["media_url"]
                        print (media_details_kind)
                        api.update_status(status="Click on the link below to download this Video\n" + video_url,auto_populate_reply_metadata = True, in_reply_to_status_id=tweet.id,)
                    except Exception as e:
                         logger.info("URL Missing")
            elif 'media' not in original_tweet.entities:
                     logger.info("This tweet does not contain a media file")
    return new_since_id

def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, since_id)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()
