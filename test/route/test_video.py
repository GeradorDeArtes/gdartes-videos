from unittest import TestCase
from app import create_app
from werkzeug.datastructures import FileStorage
from controllers.moviepy_controller import MoviepyController
import os
from config import publicdir

class TestVideo(TestCase):
    def setUp(self):
        self.app = create_app().test_client()
        self.moviepy = MoviepyController()    

    def test_positionVideoInsideImage(self):
        """
        """ 
        

    def test_overlayImage(self):
        """
        Testing if new video with overlay image is created
        """

        #mocking request post files
        video = os.path.join("public/testvideo.mp4")
        video_file = FileStorage(
            stream=open(video, "rb"),
            filename="testvideo66.mp4",
            content_type="video/mpeg",
        )

        image = os.path.join("public/testimage.jpg")
        image_file = FileStorage(
            stream=open(image, "rb"),
            filename="testimage66.jpg",
            content_type="image/jpeg",
        )

        #calling api
        rv = self.app.post(
        "/video/overlayImage",
        data={
            "video": video_file,
            "image": image_file,
            "positionX": "left",
            "positionY": "bottom"
        },
        content_type="multipart/form-data",
        follow_redirects=True
        )

        print(rv.json)

    def test_video(self):
        """
        Testing if API routing is OK
        """        
        rv = self.app.get('/video/test')
        self.assertEqual({"path": 'path_to_video'}, rv.get_json())

