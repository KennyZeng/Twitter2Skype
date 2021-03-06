#reference:https://gist.github.com/pvieytes/978125/
import time
from datetime import datetime
import re
import json as simplejson
import urllib2


class TweetParser():
    """Store the tweet info
    """
    id = None
    username = None
    url = None
    user_avatar_url = None
    tweet_url = None
    profile_url = None
    html_text = None
    retweeted = None
    retweet_user = None
    date = None
    
    def set_date(self, date_str):
        """Convert string to datetime
        """
        time_struct = time.strptime(date_str, "%a %b %d %H:%M:%S +0000 %Y")#Tue Apr 26 08:57:55 +0000 2011
        self.date = datetime.fromtimestamp(time.mktime(time_struct))
        
    
    def set_text(self, plain_text):
        """convert plain text into html text with http, user and hashtag links
        """
        
        re_http = re.compile(r"(http://[^ ]+)")
        self.html_text = re_http.sub(r'\1', plain_text)
                
        re_https = re.compile(r"(https://[^ ]+)")
        self.html_text = re_https.sub(r'\1', self.html_text)
        
        
        re_user = re.compile(r'@[0-9a-zA-Z+_]*',re.IGNORECASE)        
        for iterator in re_user.finditer(self.html_text):
            a_username = iterator.group(0)
            username = a_username.replace('@','')
            link = '' + a_username + ''
            self.html_text = self.html_text.replace(a_username, link)
                    
 
        re_hash = re.compile(r'#[0-9a-zA-Z+_]*',re.IGNORECASE)
        for iterator in re_hash.finditer(self.html_text):
            h_tag = iterator.group(0)
            link_tag = h_tag.replace('#','%23')
            link = '' + h_tag + ''
            self.html_text = self.html_text.replace(h_tag + " ", link + " ")
            #check last tag
            offset = len(self.html_text) - len(h_tag)
            index = self.html_text.find(h_tag, offset)
            if index >= 0:
                self.html_text = self.html_text[:index] + " " + link
            
 
    def set_profile_url(self):
        """Create the url profile
        """
        if self.retweeted:
            self.profile_url = "http://www.twitter.com/%s" % self.retweet_user
        else:
            self.profile_url = "http://www.twitter.com/%s" % self.username
    
    def set_tweet_url(self):
        """Create the url of the tweet
        """
        self.tweet_url = "http://www.twitter.com/%s/status/%s" % (self.username, self.id)


 
def read_tweets(user, num_tweets):
    tweets = []
    url = "http://api.twitter.com/1/statuses/user_timeline.json?screen_name=%s&count=%s&include_rts=true" % (user, num_tweets)
    file = urllib2.urlopen(url)        
    content = file.read()
    jsonContent = simplejson.loads(content)
    
    for js_tweet in jsonContent:
        tweet = TweetParser()
        tweet.id = js_tweet['id']
        tweet.username = js_tweet['user']['screen_name']
        try:
            tweet.retweet_user = js_tweet['retweeted_status']['user']['screen_name']
            tweet.retweeted = True
        except:
            tweet.retweeted = False   
        
        tweet.set_date(js_tweet['created_at'])
        #tweet.id, tweet.username must exist
        tweet.set_tweet_url()
        #convert plain text to html text
        tweet.set_text(js_tweet['text'])
        #tweet.id, tweet.username must exist
        tweet.set_profile_url()
        if tweet.retweeted:
            tweet.user_avatar_url = js_tweet['retweeted_status']['user']['profile_image_url']
        else:
            tweet.user_avatar_url = js_tweet['user']['profile_image_url']
        tweets.append(tweet)    
    return tweets

#test
"""
tweetsList =  read_tweets('GGYY', 5)
for x in tweetsList:
    print x.html_text.encode('utf8')
"""
