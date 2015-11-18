from blitzkrieg import blitzkrieg
from flask import session, jsonify
import requests, psycopg2

@blitzkrieg.route('/ping_user_data')
def ping_user_data():
    if 'user_id' not in session:
        return redirect(url_for('hello'))

    cur = blitzkrieg.db.cursor()

    cur.execute("""
            SELECT
                id,
                created_datetime
            FROM feed_data
            WHERE
                user_id = %s
                AND created_datetime::timestamp > CURRENT_TIMESTAMP
                AND created_datetime::timestamp < CURRENT_TIMESTAMP + (.25 * interval '1 minute')
        """, (session['user_id'],))
    timestamps = cur.fetchall()

    cur.close()

    return jsonify(timestamps)
