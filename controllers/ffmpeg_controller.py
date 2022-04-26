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
        ffmpegPath = "/usr/bin/ffmpeg"
        containerPath = os.path.abspath(os.path.dirname(__file__)) + "/container.png" 
        containerOutputPath = os.path.abspath(os.path.dirname(__file__)) + "/" + datetime.now().strftime("%H:%M:%S") + "container.mp4"
        
        #scale=w:h sudo -S chmod 777 videoPath
        createContainerCmd = ffmpegPath + " -i" + containerPath + " -vf scale=" + str(templateWidth) + ":" + str(templateHeight) + " "  + containerOutputPath
        createContainerProcess = subprocess.Popen(
            shlex.split(createContainerCmd)
        )
        createContainerProcess.wait()
        for line in iter(createContainerProcess.stdout.readline, b""):
            print(line)

        #position video inside container using template's position - overlay=x:y
        videoInsideContainerPath = os.path.abspath(os.path.dirname(__file__)) + "/" + datetime.now().strftime("%H:%M:%S") + "videoinsidecontainer.mp4"
        positionVideoCmd = ffmpegPath + " -i " + containerOutputPath + " -i " + videoPath + " -filter_complex '[0:v][1:v] overlay=" + str(positionX) + ":" + str(positionY) + "' " + videoInsideContainerPath
        positionVideoProcess = subprocess.Popen(
            shlex.split(positionVideoCmd), stdout=subprocess.PIPE
        )
        positionVideoProcess.wait()
        for line in iter(positionVideoProcess.stdout.readline, b""):
            print(line)

        #position image inside video at 0,0 
        finalVideoFileName =  datetime.now().strftime("%H:%M:%S") + "final.mp4"
        finalVideoPath = publicdir + finalVideoFileName
        positionImageInsideVideoCmd = ffmpegPath + " -i " + videoInsideContainerPath + " -i " + imagePath + " -filter_complex '[0:v][1:v] overlay=0:0' -c:a copy " + finalVideoPath
        positionImageInsideVideoProcess = subprocess.Popen(
            shlex.split(positionImageInsideVideoCmd)
        )
        positionImageInsideVideoProcess.wait()
        for line in iter(positionImageInsideVideoProcess.stdout.readline, b""):
            print(line)
            
        #delete unused videos
        return finalVideoFileName
        
        #ffmpeg -i container.png -vf scale=2350:2350 -t containeroutput.mp4
        #ffmpeg -i containeroutput.mp4 -i testevideo.mp4 -filter_complex "[1:v][0:v] overlay=99:51"  -c:a copy output.mp4
        # -- duplicate ffmpeg -i containeroutput.mp4 -i testevideo.mp4 -filter_complex "[0:v][1:v] overlay=99:51"  -c:a copy output.mp4
        #ffmpeg -i output.mp4 -i testeimage.png -filter_complex "[0:v][1:v] overlay=0:0"  -c:a copy output.mp4
        # -- duplicate ffmpeg -i output.mp4 -i testeimage.png -filter_complex "[0:v][1:v] overlay=0:0"  -c:a copy outputnew.mp4





