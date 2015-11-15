from blitzkrieg import blitzkrieg
from flask import render_template, request, session, url_for, redirect, jsonify
import requests, psycopg2

@blitzkrieg.route('/get_instagram_feed', methods=['GET'])
def get_instagram_feed():
    cur = blitzkrieg.db.cursor()

    result = requests.get('https://api.instagram.com/v1/users/self/feed', params={
        'access_token': session['instagram_token']
    })
    print result.json()['pagination']['next_url']

    cur.close()
    
    return result.text
