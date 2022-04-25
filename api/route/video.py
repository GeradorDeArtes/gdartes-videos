from http import HTTPStatus
from flask import Blueprint, Flask, flash, request, redirect, url_for, send_file, send_from_directory, jsonify
from flask.helpers import make_response
from flasgger import swag_from
from api.model.video import VideoModel
from api.schema.video import VideoSchema
from config import publicdir
from controllers.ffmpeg_controller import FFMPEGController
from datetime import datetime 

import os

video_api = Blueprint('video', __name__)

@video_api.route('/saveFiles', methods=['POST'])
def saveFiles():
    video_file =  request.files['video']
    video_file_ext = video_file.filename.split('.')[-1]
    video_file_name = datetime.now().strftime("%H:%M:%S") + "videofile." + video_file_ext
    video_file.save(os.path.join(publicdir, video_file_name))

    image_file = request.files['image']
    image_file_ext = image_file.filename.split('.')[-1]
    image_file_name =  datetime.now().strftime("%H:%M:%S") + "imgfile." + image_file_ext
    image_file.save(os.path.join(publicdir, image_file_name))

    paths = {
        'image_name' : image_file_name,
        'video_name' : video_file_name
    }
    
    return jsonify(paths)

@video_api.route('/getVideoFile', methods=['POST'])
def getVideoFile():
    videoName = request.form['videoName']
    return send_from_directory(publicdir, path=videoName, as_attachment=True)

@video_api.route('/overlayImage', methods=['POST'])
def overlayImage():
    """
    1 liner about the route
    A more detailed description of the endpoint
    """
    ffmpeg = FFMPEGController()    

    image_file = request.files['image']
    video_file = request.files['video']
    positionX = request.form['positionX'] 
    positionY = request.form['positionY'] 

    image_file.save(os.path.join(publicdir, image_file.filename))
    video_file.save(os.path.join(publicdir, video_file.filename))

    #position image return url with created video
    final_video_filename = ffmpeg.overlayImage(publicdir + video_file.filename, publicdir + image_file.filename, positionX, positionY)
    return send_from_directory(publicdir, path=final_video_filename, as_attachment=True)


@video_api.route('/createTemplateVideo', methods=['POST'])
def createTemplateVideo():
    ffmpeg = FFMPEGController()    

    image_file = request.files['image']
    video_file = request.files['video']

    positionX = float(request.form['positionX']) 
    positionY = float(request.form['positionY']) 
    componentHeight = float(request.form['height'])
    componentWidth = float(request.form['width'])

    image_file.save(os.path.join(publicdir, image_file.filename))
    video_file.save(os.path.join(publicdir, video_file.filename))

    #position image return url with created video
    final_video_filename = ffmpeg.positionVideoInsideImage(
        publicdir + video_file.filename, publicdir + 
        image_file.filename, 
        positionX, 
        positionY,
        componentHeight,
        componentWidth
    )
    
    return send_from_directory(publicdir, path=final_video_filename, as_attachment=True)

    
@video_api.route('/test', methods=["GET"])
def test():
    """
    API routing test
    """

    result = VideoModel("path_to_video")
    return VideoSchema().dump(result), 200

