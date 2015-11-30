from flask import Flask, render_template, request, session, url_for, redirect, jsonify
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from werkzeug.contrib.fixers import ProxyFix
import requests, psycopg2

blitzkrieg = Flask(__name__)
blitzkrieg.wsgi_app = ProxyFix(blitzkrieg.wsgi_app)

from routes import login_views
from routes import ping_views
from routes import static_website_views

conn = psycopg2.connect("dbname='dep0rlstv76jac' password='XEwbTwn0tDJ_tbDRh8qyLMB30y' user='ficmnhyayqhftm' host='ec2-107-21-219-235.compute-1.amazonaws.com' port='5432'");
#conn = psycopg2.connect("dbname='blitzkrieg' user='postgres' host='localhost' port='5432'");
conn.autocommit = True

blitzkrieg.db = conn
blitzkrieg.secret_key = 'i\x0b\x8d\r\xc2\xa83\x1dD8\x10_\xb8Q\x87\xce@\xf1k\xd6\x14\xa1\xffP'
blueprint = make_twitter_blueprint(
    api_key="3ZqiKnPeVwcNf6Z5TNYTK3Dj6",
    api_secret="lR8qWwj1orhFP2HCyyyl2KTI4uso3MmhxzonKvYQ6TKvwDfF5H",
    redirect_url="twitter_redirect"
)
blitzkrieg.register_blueprint(blueprint, url_prefix="/login")
