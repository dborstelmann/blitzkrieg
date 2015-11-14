from flask import Flask, render_template, request, session, url_for, redirect, jsonify
import requests, psycopg2, Jinja2

app = Flask(__name__)

conn = psycopg2.connect("dbname='dep0rlstv76jac' password='XEwbTwn0tDJ_tbDRh8qyLMB30y' user='ficmnhyayqhftm' host='ec2-107-21-219-235.compute-1.amazonaws.com' port='5432'");
conn.autocommit = True
cur = conn.cursor()

INSTAGRAM_CONFIG = {
    'client_id': 'e7896c47f26e463ba097362492257dd7',
    'client_secret': '2db4eb3d197e4feea21505aa2a1dcf50',
    'redirect_uri': 'https://blitzkrieg-pulse.herokuapp.com/instagram_redirect',
    'redirect_uri_local': 'https://blitzkrieg.ngrok.io/instagram_redirect'
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
            SELECT id, has_instagram FROM users WHERE email = %s AND password = %s
        """, (email, password))
    user = cur.fetchone()

    if not user:
        return jsonify({'data':'invalid_login'})

    session['user_id'] = user[0]
    session['has_instagram'] = user[1]

    return jsonify({'data':'success'})

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']

    cur.execute("""
            SELECT * FROM users WHERE email = %s
        """, (email,))
    user = cur.fetchall()

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

    cur.execute("""
            SELECT id FROM users WHERE email = %s
        """, (email,))
    (user_id,) = cur.fetchone()

    session['user_id'] = user_id
    session['has_instagram'] = False

    return jsonify({'data':'success'})

@app.route('/log_out')
def log_out():
    session.clear()
    return redirect(url_for('hello'))

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('hello'))

    if session['has_instagram']:
        cur.execute("""
                SELECT access_token FROM instagram_user WHERE user_id = %s
            """, (session['user_id'],))
        instagram_info = cur.fetchall()[0]
        if instagram_info[0]:
            session['instagram_token'] = instagram_info[0]

    return render_template('home.html')

@app.route('/instagram_redirect')
def instagram_redirect():
    result = requests.post('https://api.instagram.com/oauth/access_token', data={
        'client_id': INSTAGRAM_CONFIG['client_id'],
        'client_secret': INSTAGRAM_CONFIG['client_secret'],
        'grant_type': 'authorization_code',
        'redirect_uri': INSTAGRAM_CONFIG['redirect_uri'],
        'code': request.args.get('code')
    })
    result = result.json()
    user_info = result['user']
    session['instagram_token'] = result['access_token']

    if (session['has_instagram']):
        cur.execute("""
                UPDATE instagram_user SET access_token = %s WHERE user_id = %s
            """, (session['instagram_token'], session['user_id']))
    else:
        insert_instagram_user_query = """
                INSERT INTO instagram_user (
                        id,
                        user_id,
                        username,
                        full_name,
                        profile_picture,
                        access_token
                    )
                VALUES (%s, %s, %s, %s, %s, %s);
                UPDATE users SET has_instagram = TRUE WHERE id = %s """
        cur.execute(insert_instagram_user_query, (
            user_info['id'],
            session['user_id'],
            user_info['username'],
            user_info['full_name'],
            user_info['profile_picture'],
            result['access_token'],
            session['user_id']
        ))
        session['has_instagram'] = True

    return redirect(url_for('home'))

@app.route('/instagram_log_out', methods=['POST'])
def instagram_log_out():
    cur.execute("""
            UPDATE instagram_user SET access_token = '' WHERE user_id = %s
        """, (session['user_id'],))
    session.pop('instagram_token', None)

    return jsonify({'data':'success'})

app.secret_key = 'i\x0b\x8d\r\xc2\xa83\x1dD8\x10_\xb8Q\x87\xce@\xf1k\xd6\x14\xa1\xffP'
# When debug is true python server will update on file saves instead of needing
# to re-run server
if __name__ == '__main__':
    app.run(debug=True)
