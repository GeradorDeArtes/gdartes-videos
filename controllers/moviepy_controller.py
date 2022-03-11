from moviepy.editor import *
from config import publicdir
import os
import sys
from datetime import datetime 
from flask import send_file, send_from_directory, safe_join, abort
from moviepy.video.fx.all import crop

class MoviepyController:
    def __init__(self):
        """ 
        Self is the constructor, arguments passed here will be initialized with the object 
        """

    def overlayImage(self, videoPath, imagePath, positionX, positionY):
        """
        Needs dynamic size
        """
        video = VideoFileClip(videoPath, audio=True)
        logo = (ImageClip(imagePath)
                .set_duration(video.duration)
                .resize(height=200) # if you need to resize...
                .margin(right=8, top=8, opacity=0) # (optional) logo-border padding
                .set_position((positionX, positionY)))

        final = CompositeVideoClip([video, logo])
        file_name =  datetime.now().strftime("%H:%M:%S") + ".mp4"
        final_path = publicdir + file_name
        final.write_videofile(final_path) 
        return file_name
        #return send_from_directory(publicdir, path=file_name, as_attachment=True)

    def positionVideoInsideImage(self, videoPath, imagePath, positionX, positionY, componentHeight, componentWidth):
        """
            FUCK OFF
        """
        video = (VideoFileClip(videoPath, audio=False,)
                    .set_position((positionX, positionY)))

        #width = crop(originalClip, width=h, height=h, x_center=w/2, y_center=h/2) - WIDTH = 
        #set position can always CENTER a video
        (w, h) = video.size
        print("component size: ", componentHeight, componentWidth)
        print("original video size: ", video.w, video.h)
        video = video.resize(width=componentWidth, height= componentHeight)
        print("resized video size: ", video.w, video.h)

        if(video.h > componentHeight and video.w > componentWidth ):
            video = crop(video, height=video.h, width=video.w, x_center=w/2, y_center=h/2)
            print("cropped video size: ", video.w, video.h)
        image = ImageClip(imagePath, transparent=True).set_duration(video.duration)
        print("image size: ", image.w, image.h)
        size = (image.w, image.h)
        #create video with image
        #position actual video inside image_video
        final = CompositeVideoClip([ video, image ], size=size)
        file_name =  datetime.now().strftime("%H:%M:%S") + ".mp4"
        final_path = publicdir + file_name
        final.write_videofile(final_path, fps=24) 

        return file_name	


    def test():
        return 1
