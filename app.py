import socketio
import eventlet
from flask import Flask, render_template

sio = socketio.Server()
app = Flask(__name__)

messages = []

@app.route('/')
def index():
    return render_template('index.html')

@sio.on('connect')
def connect(sid, env):
    print('connected %s' % sid)

@sio.on('send message')
def get_message(sid, data):
    sio.emit('new message', {
        "nickname": data["nickname"],
        "body": data["body"]
    }, skip_sid=sid)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnected %s' % sid)

if __name__ == '__main__':
    app.debug = True
    sioApp = socketio.Middleware(sio, app)

    el = eventlet.wsgi.server(eventlet.listen(('', 8000)), sioApp)
    el.serve_forever()

