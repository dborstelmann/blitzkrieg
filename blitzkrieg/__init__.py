from flask import Flask, render_template, request, session, url_for, redirect, jsonify
import requests, psycopg2

blitzkrieg = Flask(__name__)

from routes import login_views
from routes import feed_views

conn = psycopg2.connect("dbname='blitzkrieg' user='postgres' host='localhost' port='5432'");
conn.autocommit = True

blitzkrieg.db = conn
blitzkrieg.secret_key = 'i\x0b\x8d\r\xc2\xa83\x1dD8\x10_\xb8Q\x87\xce@\xf1k\xd6\x14\xa1\xffP'
