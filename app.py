from flask import  Flask, redirect, url_for, send_file, send_from_directory, request, jsonify

from flasgger import Swagger
from api.route.home import home_api
from api.route.video import video_api
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, send, emit
from controllers.moviepy_controller import MoviepyController
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
    moviepy = MoviepyController()    

    positionX = float(json['positionX']) 
    positionY = float(json['positionY']) 
    componentHeight = float(json['height'])
    componentWidth = float(json['width'])
    
    #position image return url with created video
    print("creating video")
    final_video_filename = moviepy.positionVideoInsideImage(
        publicdir + json['video'], 
        publicdir + json['image'], 
        positionX, 
        positionY,
        componentHeight,
        componentWidth
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