from flask import Flask, request, Response, redirect, url_for
from functools import wraps
import urllib.request
import base64

app = Flask(__name__)

AUTHORIZED_USERNAME = 'ASIAZI2LBYV7LQTWCYUX'
AUTHORIZED_PASSWORD = 'lpSZYvNMp0+ozcynDAjCCofEEssezm/HK6PbIAuP'

def check_auth(username, password):
    return username == AUTHORIZED_USERNAME and password == AUTHORIZED_PASSWORD

def authenticate():
    return Response(
        'Login with proper credentials.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/render', methods=['GET'])
def fetch_url():
    url = request.args.get('url')

    if url:
        try:
            req = urllib.request.urlopen(url)
            data = req.read()
            req.close()
        except:
            return 'Error fetching URL'
        return data
    else:
        return 'URL parameter required'

@app.route('/flag')
@requires_auth
def flag_page():
    return "<h1>Flag Page</h1><p>Welcome to the flag page!</p> <p>FLAG{aWFtaW50aGVtZXRhZGF0YQ}<p><a href='/logout'>Logout</a>"

@app.route('/logout')
def logout():
    return Response(
        'Logged out successfully', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
