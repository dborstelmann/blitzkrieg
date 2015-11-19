import requests, psycopg2
import datetime

conn = psycopg2.connect("dbname='dep0rlstv76jac' password='XEwbTwn0tDJ_tbDRh8qyLMB30y' user='ficmnhyayqhftm' host='ec2-107-21-219-235.compute-1.amazonaws.com' port='5432'");
#conn = psycopg2.connect("dbname='blitzkrieg' user='postgres' host='localhost' port='5432'");

conn.autocommit = True

def fake_data(user_id, datetimez):
    cur = conn.cursor()

    final_feed = []

    test_date = datetime.datetime.strptime(datetimez, '%Y-%m-%d %H:%M:%S')

    for i in xrange(0, 999):
        final_feed.append((str((test_date + datetime.timedelta(minutes=i))), str(user_id)))

    cur.executemany("""INSERT INTO feed_data (created_datetime, user_id) VALUES (%s, %s)""", final_feed)

    cur.close()

    return

fake_data(5, '2015-11-18 19:45:10')
fake_data(5, '2015-11-18 19:45:20')
fake_data(5, '2015-11-18 19:45:30')
fake_data(5, '2015-11-18 19:45:40')
fake_data(5, '2015-11-18 19:45:50')
