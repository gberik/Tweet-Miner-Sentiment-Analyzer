"""
TWITTER SENTIMENT ANALYZER
@author: Galip Sina Berik
"""

#imports the necessary packages
import twitter
import re
import pickle
import dbm
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_timeline(userid):
    """Takes userid as an input and returns the Timeline of a tweeter user in raw form"""
    try:
        api = twitter.Api(consumer_key= ''#your consumer key here

                          ,consumer_secret= ''#your consumer secret here
                          ,access_token_key= '' #your access token key here
                          ,access_token_secret= ''# your access token secret here

                          #extended mode is used to have all the 240 characters after the 2017 twitter update
                          tweet_mode='extended')
    except:
        print('Authentication information is not correct')

    # change count to the number of tweets you want to get, change include_rts to True if you want retweets too.
    tweets = api.GetUserTimeline(screen_name=userid,count=30,include_rts=False)
    return tweets

def save_data(userid):
    """Saves the data downloaded by get_timeline into a database.
    Raw TimeLine of every user is saved and their 'userid' is their key
    """

    # gets raw data by running get_timeline
    data = get_timeline(userid)
    #pickles the raw data to be stores
    pickled_tweets = pickle.dumps(data)
    db = dbm.open('tweeter_database', 'c')
    #saves the pickled data to a data base and it's key will be the userid of the data
    db[userid] = pickled_tweets

def read_data(userid):
    """Reads through the database and returns the raw Timeline corresponding with
    the 'userid'
    """

    db = dbm.open('tweeter_database', 'c')
    # Reads the file in the database
    extract_data = db[userid]
    #unpickles the data for use
    unpickled_tweets = pickle.loads(extract_data)
    db.close()
    return unpickled_tweets

def get_text(userid):
    """returns only the text part of a user's timeline as a list"""
    #reads the data in the database by running read_data funciton
    raw_tweets = read_data(userid)
    tweets_list = []
    for tweet in raw_tweets:
        #takes the text part only from each tweets and append thme to a list
        tweets_text = tweet.full_text
        tweets_list.append(tweets_text)
    return tweets_list

def clean_tweet(userid):
    """Cleans the text: get's rid of links and other username mentions. Returns a list"""

    clean_tweets_list = []
    #gets the text of every tweet by running the get_text funciton
    tweets_list = get_text(userid)
    for tweet in tweets_list:
        #source of the line below: https://www.geeksforgeeks.org/twitter-sentiment-analysis-using-python/
        tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        clean_tweets_list.append(tweet)
    return clean_tweets_list

def analyze_sentiment_one_user(userid):
    """Analyzes the sentiment of the twitter user's texts. Returns numbers indicating
    the how much of the text contains negative, neutral, positive language"""
    #downloads and saves data first for future use
    save_data(userid)
    analyzer = SentimentIntensityAnalyzer()
    #runs the analyzer on the saved data
    return analyzer.polarity_scores(str(clean_tweet(userid)))

def sentiment_analyzer(*args):
    """Takes variable amounts of tweeter userid's and analyses the sentiment of their language"""
    analysis_dictionary = dict()
    # runs analyze_sentiment_one_user for each argument and stores them in a dictionary
    for i in args:
        analysis_dictionary[i]=analyze_sentiment_one_user(i)
    return analysis_dictionary

if __name__ == '__main__':
    print(sentiment_analyzer('facebook','Starbucks','Microsoft','Nike','Disney','netflix'))
