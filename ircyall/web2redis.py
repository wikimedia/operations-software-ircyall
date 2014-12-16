import json
from flask import Flask, request
from redis import StrictRedis

app = Flask(__name__)
redis = StrictRedis()


@app.route('/v1/send', methods=['POST'])
def send():
    # Validate, validate, validate!
    if 'message' not in request.form:
        return 'No message found', 400
    if 'channels' not in request.form:
        return 'No channels found', 400
    if 'token' not in request.form:
        return 'No token found', 400
    message = request.form['message']
    if message.startswith('/'):
        return 'Message starts with /, not going to process', 400
    if '\n' in message:
        message = message.split('\n')[0]  # Ignore everything after newline
    if '\r' in message:
        message = message.split('\r')[0]  # Because I'm too lazy to use a regex here >_>

    data = {
        'message': message,
        'channels': request.form.getlist('channels')
    }
    redis.rpush('ircnotifier', json.dumps(data))
    return repr(data)

if __name__ == '__main__':
    app.run(debug=True)
