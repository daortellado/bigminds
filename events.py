from better_profanity import profanity
from flask_socketio import emit, send

from datetime import datetime
import json

from models import Instance, Message, ClassNotiQueue, Channel
from app import database, socketio

# Faster to initialize variable here vs doing it every function call, per library documentation.
profanity.load_censor_words()

@socketio.on('message')
def handle_message(msg):
    global profane
    name = msg['name']
    content = msg['message']

    name_cleaned = profanity.censor(name)
    content_cleaned = profanity.censor(content)

    now = datetime.now().strftime('%A %I:%M:%S %p').lstrip("0").replace(" 0", " ")

    message_object = Message(name=name_cleaned, content=content_cleaned, date_posted=now)
    database.session.add(message_object)
    database.session.commit()

    json_data = {
        'name' : name_cleaned,
        'content' : content_cleaned,
        'date' : now
    }

    send({'json_data' : json_data}, broadcast=True)

@socketio.on('channel')
def handle_channel(chn):
    global profane
    name = chn['name']
    content = chn['message']

    name_cleaned = profanity.censor(name)
    content_cleaned = profanity.censor(content)

    now = datetime.now().strftime('%A %I:%M:%S %p').lstrip("0").replace(" 0", " ")

    message_object = Channel(name=name_cleaned, content=content_cleaned, date_posted=now)
    database.session.add(message_object)
    database.session.commit()

    json_chan = {
        'name' : name_cleaned,
        'content' : content_cleaned,
        'date' : now
    }

    socketio.emit('channel', json_chan)