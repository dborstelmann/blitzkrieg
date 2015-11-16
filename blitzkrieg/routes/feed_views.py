from blitzkrieg import blitzkrieg
from flask import render_template, request, session, url_for, redirect, jsonify
import requests, psycopg2
import datetime

@blitzkrieg.route('/get_instagram_feed', methods=['GET'])
def get_instagram_feed():
    cur = blitzkrieg.db.cursor()

    data_feed = []
    final_feed = recursive_results(data_feed)
    import pdb; pdb.set_trace()

    print(len(final_feed))
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
        if created_date < datetime.datetime.now()-datetime.timedelta(days=1):
            break_check = True
            break
        else:
            data_feed.append(point)

    if break_check:
        import pdb; pdb.set_trace()
        
        return data_feed
    else:
        print('trying again')
        next_url = result['pagination']['next_url']
        recursive_results(data_feed, next_url)
