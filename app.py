from flask import  Flask, redirect, url_for, send_file, send_from_directory, request, jsonify

from flasgger import Swagger
from api.route.home import home_api
from api.route.video import video_api
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, send, emit
from controllers.ffmpeg_controller import FFMPEGController
from config import publicdir

import os
import json as pyjson

def create_app():
    app = Flask(__name__)
    CORS(app)
    Swagger(app)

    app.config['SWAGGER'] = {
        'title': 'Moviepy API interface',
    }
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SECRET_KEY'] = 'secret!'
    app.config.from_pyfile('config.py')
    app.register_blueprint(video_api, url_prefix='/video')

    return app

app = create_app()
socketio = SocketIO(app, cors_allowed_origins="*") 

@socketio.on('video')
def handle_video(json):
    ffmpeg = FFMPEGController()    

    positionX = float(json['positionX']) 
    positionY = float(json['positionY']) 
    componentHeight = float(json['height'])
    componentWidth = float(json['width'])
    templateWidth = float(json['templateWidth'])
    templateHeight = float(json['templateHeight'])

    #position image return url with created video
    final_video_filename = ffmpeg.positionVideoInsideImage(
        publicdir + json['video'], 
        publicdir + json['image'], 
        positionX, 
        positionY,
        componentHeight,
        componentWidth,
        templateWidth,
        templateHeight
    )

    final_video = {
        'final_video_name': final_video_filename
    }
    
    final_video_json = pyjson.dumps(final_video)
    emit('video', final_video_json)

"""
standart flask api
def create_app():
    app = Flask(__name__)
    cors = CORS(app)

    app.config['SWAGGER'] = {
        'title': 'Moviepy API interface',
    }
    app.config['CORS_HEADERS'] = 'Content-Type'
    swagger = Swagger(app)
     ## Initialize Config
    app.config.from_pyfile('config.py')
    app.register_blueprint(home_api, url_prefix='/api')
    app.register_blueprint(video_api, url_prefix='/video')

    return app

app = create_app()
"""


#https://livecodestream.dev/post/python-flask-api-starter-kit-and-project-layout/
#pipenv run python -m flask run
#pipenv run python -m unittest