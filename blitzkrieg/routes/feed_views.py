import requests, psycopg2
import datetime

conn = psycopg2.connect("dbname='dep0rlstv76jac' password='XEwbTwn0tDJ_tbDRh8qyLMB30y' user='ficmnhyayqhftm' host='ec2-107-21-219-235.compute-1.amazonaws.com' port='5432'");
#conn = psycopg2.connect("dbname='blitzkrieg' user='postgres' host='localhost' port='5432'");

conn.autocommit = True

def get_users():
    cur = conn.cursor()

    cur.execute("""
            SELECT user_id, access_token FROM instagram_user WHERE access_token <> ''
        """)
    users = cur.fetchall()

    for user in users:
        get_instagram_feed(user[0], user[1])

    cur.close()


def get_instagram_feed(user_id, access_token):
    cur = conn.cursor()

    data_feed = []
    final_feed = recursive_results(data_feed, user_id, access_token)

    # when doing this change timedelta to days=1
    # print(len(final_feed))
    cur.executemany("""INSERT INTO feed_data (created_datetime, user_id) VALUES (%s, %s)""", final_feed)
    # print('done')

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
        if created_date < datetime.datetime.now() - datetime.timedelta(minutes=60):
            break_check = True
            break
        else:
            data_feed.append((str(created_date + datetime.timedelta(minutes=10)), str(user_id)))

    if break_check:
        return data_feed
    else:
        next_url = result['pagination']['next_url']
        return recursive_results(data_feed, user_id, access_token, next_url)


get_users()
