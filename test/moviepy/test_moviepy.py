from unittest import TestCase
from controllers.moviepy_controller import MoviepyController
from config import publicdir

class TestMoviepyController(TestCase):
    def setUp(self):
        self.moviepy = MoviepyController()    

    def test_overlayImage(self):
        """
        Tests the route screen message
        """
        video_path = publicdir + "testvideo.mp4"
        image_path = publicdir + "testimage.jpg"
        positionX = "left"
        positionY = "bottom"
        print('words')
        #self.moviepy.positionImage(video_path, image_path, positionX, positionY)
        #self.assertTrue(x, 1)

    
    def test_positionVideoInsideImage(self):
        """
        """ 
        self.moviepy.positionVideoInsideImage(publicdir + "testvideo.mp4", publicdir + 'test_top_bottom.png')