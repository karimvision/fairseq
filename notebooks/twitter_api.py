from time import time, sleep
from math import ceil
import twitter

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
MAX_REQUESTS_PER_WINDOW = 180 # per 15 min
MAX_POSTS_PER_CALL = 100
class Twitter():
    def __init__(self):
        self.api = twitter.Api(consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token_key=access_token,
                          access_token_secret=access_token_secret, tweet_mode= 'extended')
        
    def get_tweets(self, search_term, count=100,max_id=None):
        num_calls_required = ceil(count/MAX_POSTS_PER_CALL)
        num_sleeps_required = int(num_calls_required/MAX_REQUESTS_PER_WINDOW)
        print("{} requests and {} 15 min sleeps required".format(num_calls_required,num_sleeps_required ))
        TIMEOUT = count*0.03 +  num_sleeps_required*(15*60)# assuming 3 sec max per api call and num sleeps required
        tweets = []
        num_requests = 0
        start_time = time()
        while len(tweets) < count:
            if time() - start_time > TIMEOUT:
                print("timeout reached")
                break
            if num_requests == MAX_REQUESTS_PER_WINDOW:
                print("Max requests per window reached. Sleeping ...")
                sleep(15*60) # sleep 15 min and try again
                num_requests = 0
                
            # max 100 count per call
            api_result = self.api.GetSearch(search_term, count=MAX_POSTS_PER_CALL, lang="en",max_id=max_id)
            num_requests +=1
            max_id = api_result[-1].AsDict()['id']
            for t in api_result:
                if t.retweeted_status:
                    tweets.append(t.retweeted_status.full_text)
                else:
                    tweets.append(t.full_text)
            tweets.extend([t.full_text ])
        print("Time Taken {} Seconds".format(time()-start_time))
        return tweets
