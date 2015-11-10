from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/instagram_redirect', methods=['GET'])
def instagram_redirect():
    r = requests.post("https://api.instagram.com/oauth/access_token",
        data = {
            "client_id":"e7896c47f26e463ba097362492257dd7",
            "client_secret":"2db4eb3d197e4feea21505aa2a1dcf50",
            "grant_type":"authorization_code",
            "redirect_uri":"https://blitzkrieg-pulse.herokuapp.com/instagram_redirect",
            "code":request.GET['code'],
        }
    )

    print(r)
    return render_template('hello.html')

# When debug is true python server will update on file saves instead of needing
# to re-run server
if __name__ == '__main__':
    app.run(debug=True)
