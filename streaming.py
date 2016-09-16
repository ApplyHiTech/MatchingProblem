# Data collection from Twitter from Streaming API
# Written by Rohit Jain
from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from config import Mongo
import json, time

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="cx6rfiAkwydid1ShZZ3ihSYbd"
consumer_secret="dGELgca5zgWVmu7kpnpOvxuJmFxmHibXe2NajhRx4Pj8DPh5yS"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="177630113-RFjraxYOVFEyphacPtciaLjqOIzRfRg5KAic7btk"
access_token_secret="yoZ9nIJYe3mNWcHfQGxvZC9AgEwL6Gt70TwzCaFSk3iPM"

db = Mongo()
count = 1

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        datum = json.loads(data)
        try:
            #print("insert")
            db.tweets.insert(datum)
        except Exception as e:
            print(e)
        return True

    def on_error(self, status):
        print(status)
        print("sleeping")
        time.sleep(60*count)
        count = count*count + 1

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['instagram'],locations=[-74.2,40.4,-73.7,40.9], async=True)
