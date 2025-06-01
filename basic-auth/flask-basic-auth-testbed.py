'''
basic flask app to test basic auth spray script
'''

from flask import Flask, request, Response

app = Flask(__name__)

# Define credentials
USERNAME = 'example-username'
PASSWORD = 'example-password'


def check_auth(username, password):
    return username == USERNAME and password == PASSWORD


def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__ 
    return decorated

@app.route('/')
@requires_auth
def index():
    return "Hello, you have accessed the protected index page!"

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8080,debug=False)
