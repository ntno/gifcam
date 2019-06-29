import os
from twython import Twython

APP_KEY = os.getenv('TWITTER_APP_KEY')
APP_SECRET = os.getenv('TWITTER_APP_SECRET')
OAUTH_TOKEN = os.getenv('TWITTER_OAUTH_TOKEN')
OAUTH_TOKEN_SECRET = os.getenv('TWITTER_OAUTH_TOKEN_SECRET')

#setup the twitter api client
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def tweet_pic(filename, message):
    try:
        print('Posting to Twitter')
        photo = open(filename, 'rb')
        response = twitter.upload_media(media=photo)
        twitter.update_status(status=message, media_ids=[response['media_id']])
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    tweet_pic("./gifs/ntno.gif", "hello world")