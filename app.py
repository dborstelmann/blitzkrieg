from flask import Flask, render_template, request, session, url_for, redirect, jsonify
import requests, psycopg2

app = Flask(__name__)

try:
    conn = psycopg2.connect("dbname='blitzkrieg' user='postgres' host='localhost' port='5432'");
except:
    print "I am unable to connect to the database"
cur = conn.cursor()

INSTAGRAM_CONFIG = {
    'client_id': 'e7896c47f26e463ba097362492257dd7',
    'client_secret': '2db4eb3d197e4feea21505aa2a1dcf50',
    'redirect_uri': 'https://blitzkrieg-pulse.herokuapp.com/instagram_redirect'
}

@app.route('/')
def hello():
    if 'user_id' in session:
        return redirect(url_for('home'))
    else:
        return render_template('hello.html')

@app.route('/log_in', methods=['POST'])
def log_in():
    email = request.form['email']
    password = request.form['password']

    cur.execute("""
            SELECT id FROM users WHERE email = '{0}' AND password = '{1}'
        """.format(email, password))
    user = cur.fetchone()
    conn.commit()

    if not user:
        return jsonify({'data':'invalid_login'})

    session['user_id'] = user[0]

    return jsonify({'data':list(session)})

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']

    cur.execute("""
            SELECT * FROM users WHERE email = '{0}'
        """.format(email))
    user = cur.fetchall()
    conn.commit()

    if len(user) > 0:
        return jsonify({'data':'user_exists_error'})

    insert_user_query = """
            INSERT INTO users (
                    first_name,
                    last_name,
                    email,
                    password
                )
            VALUES (%s, %s, %s, %s) """
    cur.execute(insert_user_query, (first_name, last_name, email, password))
    conn.commit()

    cur.execute("""
            SELECT id FROM users WHERE email = '{0}'
        """.format(email))
    (user_id,) = cur.fetchone()
    conn.commit()

    session['user_id'] = user_id

    return jsonify({'data':list(session)})

@app.route('/log_out')
def log_out():
    session.clear()
    return redirect(url_for('hello'))

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('hello'))
    return render_template('home.html')

app.secret_key = 'i\x0b\x8d\r\xc2\xa83\x1dD8\x10_\xb8Q\x87\xce@\xf1k\xd6\x14\xa1\xffP'
# When debug is true python server will update on file saves instead of needing
# to re-run server
if __name__ == '__main__':
    app.run(debug=True)
