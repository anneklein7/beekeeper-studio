import logging
from pathlib import Path
import azure.functions as func
import tweepy
import requests
import csv
import os
import random


ROOT = Path("Macintosh HD:/Users/annechafer/epigram_bot/callimachus_file.csv").resolve().parents[0]



def get_tweet(tweets_file, excluded_tweets=None):
    # Get tweet to post from CSV file

    with open(tweets_file) as csvfile:
        reader = csv.DictReader(csvfile)
        possible_tweets = [row["tweet"] for row in reader]

    if excluded_tweets:
        recent_tweets = [status_object.text for status_object in excluded_tweets]
        possible_tweets = [tweet for tweet in possible_tweets if tweet not in recent_tweets]

    selected_tweet = random.choice(possible_tweets)

    return selected_tweet

consumer_key = "6uCHzKRPTU4XUxZoj2J5DhnQh"
consumer_secret = "7NXQ8wh3jaIyyaFsNhyndBpnQBmMnARVuL9JVmu049FoS9RAug"
access_token = "105142860-MzcM2Jmv7WXopfEOTdgECrzXJ3k0zeaB8N3WmjJo"
access_token_secret = "1WDsI2KJFqzbSOh7DGZCZ5UdEOj4DvoUjA0nolqKF2202"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def tweet_quote():
    tweet = get_quote()
    status = api.update_status(tweet)
    print(status.id)
# post the tweets using a function


tweet_quote()


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
