import subprocess
from config import publicdir
from datetime import datetime 
import os
import shlex

class FFMPEGController:
    def __init__(self):
        """ 
        Self is the constructor, arguments passed here will be initialized with the object 
        """

    def positionVideoInsideImage(self, videoPath, imagePath, positionX, positionY, componentHeight, componentWidth, templateWidth, templateHeight):
        #create container with templates dimensions 
        containerPath = os.path.abspath(os.path.dirname(__file__)) + "/container.png" 
        containerOutputPath = os.path.abspath(os.path.dirname(__file__)) + "/" + datetime.now().strftime("%H:%M:%S") + "container.mp4"
        
        #scale=w:h sudo -S chmod 777 videoPath
        #createContainerCmd = "ffmpeg -i " + containerPath + " -vf scale=" + str(templateWidth) + ":" + str(templateHeight) + " "  + containerOutputPath
        createContainerProcess = subprocess.Popen([
            "ffmpeg", "-i", containerPath, "-vf", 
            "scale=" + str(templateWidth) + ":" + str(templateHeight),
            containerOutputPath])
        createContainerProcess.wait()

        #position video inside container using template's position - overlay=x:y
        videoInsideContainerPath = os.path.abspath(os.path.dirname(__file__)) + "/" + datetime.now().strftime("%H:%M:%S") + "videoinsidecontainer.mp4"
        positionVideoCmd = "ffmpeg -i " + containerOutputPath + " -i " + videoPath + " -filter_complex '[0:v][1:v] overlay=" + str(positionX) + ":" + str(positionY) + "' " + videoInsideContainerPath
        positionVideoProcess = subprocess.Popen(
            shlex.split(positionVideoCmd)
        )
        positionVideoProcess.wait()

        #position image inside video at 0,0 
        finalVideoFileName =  datetime.now().strftime("%H:%M:%S") + "final.mp4"
        finalVideoPath = publicdir + finalVideoFileName
        positionImageInsideVideoCmd = "ffmpeg -i " + videoInsideContainerPath + " -i " + imagePath + " -filter_complex '[0:v][1:v] overlay=0:0' -c:a copy " + finalVideoPath
        positionImageInsideVideoProcess = subprocess.Popen(
            shlex.split(positionImageInsideVideoCmd)
        )
        positionImageInsideVideoProcess.wait()

        #delete unused videos
        return finalVideoFileName
        
        #ffmpeg -i container.png -vf scale=2350:2350 -t containeroutput.mp4
        #ffmpeg -i containeroutput.mp4 -i testevideo.mp4 -filter_complex "[1:v][0:v] overlay=99:51"  -c:a copy output.mp4
        # -- duplicate ffmpeg -i containeroutput.mp4 -i testevideo.mp4 -filter_complex "[0:v][1:v] overlay=99:51"  -c:a copy output.mp4
        #ffmpeg -i output.mp4 -i testeimage.png -filter_complex "[0:v][1:v] overlay=0:0"  -c:a copy output.mp4
        # -- duplicate ffmpeg -i output.mp4 -i testeimage.png -filter_complex "[0:v][1:v] overlay=0:0"  -c:a copy outputnew.mp4





