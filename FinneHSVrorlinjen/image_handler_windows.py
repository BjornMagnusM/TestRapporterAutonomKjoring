try:
    from .image_methods import ImageMethods  # Attempt relative import for package context
except ImportError:
    from image_methods import ImageMethods  # Fallback to direct import for standalone execution

import cv2
import numpy as np
import time
import subprocess
import cv2.aruco as aruco



video_path = "VideoRor.mp4"

class ImageHandler:
    def __init__(self):
        self.hsv_range_bib = {
            "pipeline_sim" : [[30,114,114],[30,255,255]],
            "visual_short_distance" : [[0, 0, 30],[86, 0, 120]],
            "visual_long_distance" : [[0, 0, 0],[40, 200, 170]],
            "Pipeline_video" : [[77,43,165],[91,116,207]],
        }
        self.feed_image = None
        self.feed_image2 = None
        self.show_hsv = None
        self.cooldown = 0
        self.Id_list= []   
        self.filtered_list = []
        self.aruco_printed = 0 
        self.bench_box_image = None
        self.scale_factor = 0.5
        
    def show_image(self, double):
        if not double:
            ImageMethods.showImage(self.feed_image)
        else:
            showImage = ImageMethods.stack_images([self.feed_image,self.feed_image2])
            ImageMethods.showImage(showImage)
        
        

    def find_pipeline(self,cap):
        image_edit = ImageMethods.scale_image(cap, scale_factor=self.scale_factor)
        self.dims = image_edit.shape
        hsv_range = self.hsv_range_bib["Pipeline_video"]
        hsv_image = ImageMethods.color_filter(image_edit , hsv_range)
        try:
            cv2.line(hsv_image,(0,int(self.dims[0]/2)),(self.dims[1],int(self.dims[0]/2)),(0,0,0),10)     
            box_list = ImageMethods.find_boxes(hsv_image, image_edit, 600, True)
            highest_box = ImageMethods.find_highest_box(box_list)
            if highest_box is None:done = True
            else:done=False
            angle_deg = ImageMethods.find_angle_box(highest_box,90, self.dims[1])
            angle_deg, self.cooldown = ImageMethods.angle_cooldown(angle_deg,self.cooldown)
            center_x,center_y = ImageMethods.find_Center(image_edit,highest_box, True)
        except Exception as e:_ = e
        cv2.putText(image_edit, f"{int(angle_deg)}",[800,525], cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 2, cv2.LINE_AA)
        ImageMethods.showImage(image_edit)
        return angle_deg,center_x, done
  



    def aruco_handler(self,image1, image2=None):
        self.Id_list= ImageMethods.read_AruCo(image1,self.Id_list)
        if image2 is not None:
            self.Id_list = ImageMethods.read_AruCo(image2,self.Id_list)

    def filter_arucos(self):
        self.filtered_list = ImageMethods.filtered_ids_list(self.Id_list)
    

handler = ImageHandler()

# Specify the path to your MP4 file

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video was opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Read and display the video frame by frame
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # If frame is read correctly, ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Display the resulting frame
    angle_deg,center_x, done= handler.find_pipeline(frame)


    # Press 'q' on the keyboard to exit
    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the video capture object and close all frames
cap.release()
cv2.destroyAllWindows()
