from blitzkrieg import blitzkrieg
from flask import render_template, request, session, url_for, redirect, jsonify
import requests, psycopg2
import datetime

@blitzkrieg.route('/get_instagram_feed', methods=['GET'])
def get_instagram_feed():
    cur = blitzkrieg.db.cursor()

    data_feed = []
    final_feed = recursive_results(data_feed)

    # when doing this change timedelta to days=1
    # print(len(final_feed))
    cur.executemany("""INSERT INTO feed_data (created_datetime) VALUES (%s)""", final_feed)
    # print('done')

    cur.close()

    return jsonify({'data':'success'})


def recursive_results(data_feed, next_url=None):

    if next_url:
        result = requests.get(next_url).json()
    else:
        result = requests.get('https://api.instagram.com/v1/users/self/feed', params={
            'access_token': session['instagram_token']
        }).json()

    break_check = False

    for point in result['data']:
        created_date = datetime.datetime.fromtimestamp(int(point['created_time']))
        if created_date < datetime.datetime.now() - datetime.timedelta(minutes=10):
            break_check = True
            break
        else:
            data_feed.append((str(created_date + datetime.timedelta(minutes=10)),))

    if break_check:
        return data_feed
    else:
        next_url = result['pagination']['next_url']
        return recursive_results(data_feed, next_url)
