import requests, psycopg2
import datetime
from twitter import *
from flask_dance.contrib.twitter import twitter

TWITTER_CONFIG = {
    'consumer_key': '3ZqiKnPeVwcNf6Z5TNYTK3Dj6',
    'consumer_secret': 'lR8qWwj1orhFP2HCyyyl2KTI4uso3MmhxzonKvYQ6TKvwDfF5H',
}

conn = psycopg2.connect("dbname='dep0rlstv76jac' password='XEwbTwn0tDJ_tbDRh8qyLMB30y' user='ficmnhyayqhftm' host='ec2-107-21-219-235.compute-1.amazonaws.com' port='5432'");
#conn = psycopg2.connect("dbname='blitzkrieg' user='postgres' host='localhost' port='5432'");

conn.autocommit = True

def get_users():
    cur = conn.cursor()

    cur.execute("""
            SELECT user_id, access_token, access_token_secret FROM twitter_user WHERE access_token <> ''
        """)
    twit_users = cur.fetchall()

    cur.execute("""
            SELECT user_id, access_token FROM instagram_user WHERE access_token <> ''
        """)
    insta_users = cur.fetchall()

    for user in twit_users:
        get_twitter_feed(user[0], user[1], user[2])

    for user in insta_users:
        get_instagram_feed(user[0], user[1])

    cur.close()

def get_twitter_feed(user_id, access_token, access_token_secret):
    cur = conn.cursor()

    t = Twitter(auth=OAuth(access_token, access_token_secret, TWITTER_CONFIG['consumer_key'], TWITTER_CONFIG['consumer_secret']))

    data_feed = []
    final_feed = twitter_recursion(t, data_feed, user_id)

    cur.executemany("""INSERT INTO feed_data (created_datetime, user_id, api_service) VALUES (%s, %s, 'twitter')""", final_feed)

    cur.close()

    return

def twitter_recursion(t, data_feed, user_id, max_id=None):

    if max_id:
        home_tweets = t.statuses.home_timeline(max_id=max_id, exclude_replies=True)
    else:
        home_tweets = t.statuses.home_timeline(exclude_replies=True)

    break_check = False

    if max_id:
        home_tweets.pop(0)

    for tweet in home_tweets:
        print(tweet['id'])
        created_date = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y') - datetime.timedelta(hours=6)
        if created_date < datetime.datetime.now() - datetime.timedelta(minutes=1000):
            break_check = True
            break
        else:
            data_feed.append((str(created_date + datetime.timedelta(minutes=10)), str(user_id)))

    if break_check:
        return data_feed
    else:
        max_id = home_tweets[len(home_tweets) - 1]['id']
        return twitter_recursion(t, data_feed, user_id, max_id)

def get_instagram_feed(user_id, access_token):
    cur = conn.cursor()

    data_feed = []
    final_feed = recursive_results(data_feed, user_id, access_token)

    cur.executemany("""INSERT INTO feed_data (created_datetime, user_id, api_service) VALUES (%s, %s, 'instagram')""", final_feed)

    cur.close()

    return

def recursive_results(data_feed, user_id, access_token, next_url=None):

    if next_url:
        result = requests.get(next_url).json()
    else:
        result = requests.get('https://api.instagram.com/v1/users/self/feed', params={
            'access_token': access_token
        }).json()

    break_check = False

    for point in result['data']:
        created_date = datetime.datetime.fromtimestamp(int(point['created_time']))
        if created_date < datetime.datetime.now() - datetime.timedelta(minutes=10):
            break_check = True
            break
        else:
            data_feed.append((str(created_date + datetime.timedelta(minutes=10)), str(user_id)))

    if break_check:
        return data_feed
    else:
        next_url = result['pagination']['next_url']
        return recursive_results(data_feed, user_id, access_token, next_url)

def delete_old_stuff():
    cur = conn.cursor()

    cur.execute("""
            DELETE FROM feed_data
            WHERE created_datetime::timestamp < CURRENT_TIMESTAMP - (20 * interval '1 minute')
        """)

    cur.close()

get_users()
delete_old_stuff()
