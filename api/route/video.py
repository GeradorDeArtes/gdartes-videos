from http import HTTPStatus
from flask import Blueprint, Flask, flash, request, redirect, url_for, send_file, send_from_directory
from flask.helpers import make_response
from flasgger import swag_from
from api.model.video import VideoModel
from api.schema.video import VideoSchema
from config import publicdir
from controllers.moviepy_controller import MoviepyController
import os

video_api = Blueprint('video', __name__)


@video_api.route('/overlayImage', methods=['POST'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Position image over video',
            'schema': VideoSchema
        }
    }
})
def overlayImage():
    """
    1 liner about the route
    A more detailed description of the endpoint
    """
    moviepy = MoviepyController()    

    image_file = request.files['image']
    video_file = request.files['video']
    positionX = request.form['positionX'] 
    positionY = request.form['positionY'] 

    image_file.save(os.path.join(publicdir, image_file.filename))
    video_file.save(os.path.join(publicdir, video_file.filename))

    #position image return url with created video
    final_video_filename = moviepy.overlayImage(publicdir + video_file.filename, publicdir + image_file.filename, positionX, positionY)
    return send_from_directory(publicdir, path=final_video_filename, as_attachment=True)
    #print(final_video_url)
    #result = VideoModel(final_video_url)

    #return VideoSchema().dump(result), 200

@video_api.route('/createTemplateVideo', methods=['POST'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Create video using template image',
            'schema': VideoSchema
        }
    }
})
def createTemplateVideo():
    moviepy = MoviepyController()    

    image_file = request.files['image']
    video_file = request.files['video']

    positionX = float(request.form['positionX']) 
    positionY = float(request.form['positionY']) 
    componentHeight = float(request.form['height'])
    componentWidth = float(request.form['width'])

    image_file.save(os.path.join(publicdir, image_file.filename))
    video_file.save(os.path.join(publicdir, video_file.filename))

    #position image return url with created video
    final_video_filename = moviepy.positionVideoInsideImage(
        publicdir + video_file.filename, publicdir + 
        image_file.filename, 
        positionX, 
        positionY,
        componentHeight,
        componentWidth
    )
    
    return send_from_directory(publicdir, path=final_video_filename, as_attachment=True)

    
@video_api.route('/test', methods=["GET"])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'API endpoint test',
            'schema': VideoSchema
        }
    }
})
def test():
    """
    API routing test
    """

    result = VideoModel("path_to_video")
    return VideoSchema().dump(result), 200


"""
url arg example 
@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename) 
"""

