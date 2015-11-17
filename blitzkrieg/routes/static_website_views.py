from blitzkrieg import blitzkrieg
from flask import render_template

@blitzkrieg.route('/about')
def static_website():
    return render_template('static_website.html')
