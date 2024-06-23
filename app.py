from flask import Flask, request, Response, redirect, url_for
from functools import wraps
import urllib.request
import base64

app = Flask(__name__)

# 인증 정보
AUTHORIZED_USERNAME = 'ASIAZI2LBYV7LQTWCYUX'
AUTHORIZED_PASSWORD = 'lpSZYvNMp0+ozcynDAjCCofEEssezm/HK6PbIAuP'

# HTTP Basic Authentication 체크 데코레이터
def check_auth(username, password):
    return username == AUTHORIZED_USERNAME and password == AUTHORIZED_PASSWORD

def authenticate():
    """인증 실패 시 401 에러를 반환"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# 플래그 페이지
@app.route('/flag')
@requires_auth
def flag_page():
    return "<h1>Flag Page</h1><p>Welcome to the flag page!</p> <p>FLAG{aWFtaW50aGVtZXRhZGF0YQ}<p><a href='/logout'>Logout</a>"

# 로그아웃 엔드포인트
@app.route('/logout')
def logout():
    return Response(
        'Logged out successfully', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
