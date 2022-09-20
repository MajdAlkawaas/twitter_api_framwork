import os
import csv
import tweepy
import pandas as pd
import numpy as np
from decouple import config


API_KEY       = config('API_KEY')
API_SECRETS   = config('API_SECRETS')
ACCESS_TOKEN  = config('ACCESS_TOKEN')
ACCESS_SECRET = config('ACCESS_SECRET')



# Authenticate to Twitter
auth = tweepy.OAuthHandler(API_KEY,API_SECRETS)
auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET) 
api = tweepy.API(auth)
 
try:
	api.verify_credentials()
	print('Successful Authentication')
except:
	print('Failed authentication')



# function to perform data extraction
def scrape_by_hashtag(hashtag, date_since, numtweet, filename = 'scraped_tweets.csv'):
	"""
	The function retrives tweets from the twitter API and saves them in a csv file
	Parameters:
	hashtag    (string): the hashtage which you want to retrive tweets about.
	date_since (string): starting date till now for the tweets in the format yyyy-mm-dd
	numtweet   (int)   : number of tweets to be retrived
	filename   (string): path where we want the file to be stored at

	Returns:
	dataframe: retrived tweets
	"""
	# Creating DataFrame using pandas
	db = pd.DataFrame(columns=['username', 'description', 'location', 'text', 'hashtags'])

	# .Cursor() used to search through twitter for
	# the required tweets. The number of tweets can be
	# restricted using .items(number of tweets)
	tweets = tweepy.Cursor(api.search_tweets, q = hashtag, lang="en",
						since_id=date_since, tweet_mode='extended').items(numtweet)


	# .Cursor() returns an iterable object. Each item in
	# the iterator has the tweet's requested attributes 
	list_tweets = [tweet for tweet in tweets]

	# we will iterate over each tweet in the
	# list for extracting information about each tweet
	for tweet in list_tweets:
		username     = tweet.user.screen_name
		description  = tweet.user.description
		location     = tweet.user.location
		hashtags     = tweet.entities['hashtags']

		# Retweets can be distinguished by a retweeted_status attribute,
		# in case it is an invalid reference, except block will be executed
		try:
			text = tweet.retweeted_status.full_text
		except AttributeError:
			text = tweet.full_text
		hashtext = list()
		for j in range(0, len(hashtags)):
			hashtext.append(hashtags[j]['text'])

		# Appending all the extracted information in the DataFrame
		ith_tweet = [username, description, location, text, hashtext]
		db.loc[len(db)] = ith_tweet

	# we will save our database as a CSV file.
	db.to_csv(filename)
	return db 