from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# When debug is true python server will update on file saves instead of needing
# to re-run server
if __name__ == '__main__':
    app.run(debug=True)
