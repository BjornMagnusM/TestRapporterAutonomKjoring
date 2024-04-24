from image_methods import ImageMethods  
import cv2
import numpy as np
import cv2.aruco as aruco
import time 



video_path = "Benk.mp4"
class ImageHandler:
    def __init__(self):
        self.hsv_range_bib = {
            "pipeline_sim" : [[30,114,114],[30,255,255]],
            "visual_short_distance" : [[0, 0, 30],[86, 0, 120]],
            "visual_long_distance" : [[0, 0, 0],[40, 200, 170]],
            "Pipeline_video" : [[46,35,183],[89,101,229]],
            "Benk_video" : [[0,121,124],[36,255,237]],
            "Benk_video2" : [[0,85,141],[38,255,237]],
            "Benk_video3" : [[0,87,150],[38,255,248]],
            "Benk_video4" : [[0,38,38],[31,255,255]],
            "Benk_video5" : [[0,24,179],[49,255,238]],
        }
        self.feed_image = None
        self.feed_image2 = None
        self.show_hsv = None
        self.cooldown = 0
        self.Id_list= []   
        self.filtered_list = []
        self.aruco_printed = 0 
        self.bench_box_image = None
        self.scale_factor = 1
        
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
        hsv_image = ImageMethods.close_image(hsv_image,10)
        try:
            cv2.line(hsv_image,(0,int(self.dims[0]/2)),(self.dims[1],int(self.dims[0]/2)),(0,0,0),10)     
            box_list = ImageMethods.find_boxes(hsv_image, image_edit, 10000, True)
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
  


    def find_bench(self, cap):
        size = 0.0
        positions = None
        angle = None
        #Copy and scale current imagefeeds
        image_edit = ImageMethods.scale_image(cap, scale_factor=self.scale_factor)
        image_edit2 = ImageMethods.scale_image(cap, scale_factor=self.scale_factor)
        #Check for AruCo-codes
        #self.aruco_handler(image_edit, image_edit2)
        #retrieve image dimentions
        self.dims = image_edit.shape
        #Apply HSV mask to make a binary image
        hsv_range = self.hsv_range_bib["Benk_video5"]
        hsv_image = ImageMethods.color_filter(image_edit , hsv_range)
        #Try to find bench by finding the biggest box.
        #Find the angle and size of the box to decide distance and yaw relative to bench
        try:
            boxes = ImageMethods.find_boxes(hsv_image, image_edit, 500, False)
            bench = ImageMethods.find_biggest_box(image_edit, boxes, True) 
            positions, area = ImageMethods.get_box_info(bench)
            angle, angle_deg = ImageMethods.find_angle_box(bench,180, self.dims[1])
            #Back of bench is smaller than front, this makes for a different distance measure in pixels.
            #if front:size = (self.scale_factor**2)*80000/area
            size = (self.scale_factor**2)*160000/area
        except Exception as e:_ = e #Display camerafeeds no matter if bench is found or not.
        
    # Overlay time on the video
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image_edit2, f"Time: {current_time:.2f}s", (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        showImage = ImageMethods.stack_images([image_edit,image_edit2])
        ImageMethods.showImage(showImage)
        return size, positions, angle #return relevant positional data.


    def aruco_handler(self,image1, image2=None):
        self.Id_list= ImageMethods.read_AruCo(image1,self.Id_list)
        if image2 is not None:
            self.Id_list = ImageMethods.read_AruCo(image2,self.Id_list)

    def filter_arucos(self):
        self.filtered_list = ImageMethods.filtered_ids_list(self.Id_list)

# Open the video file
cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frames per second of the video
pause = False
delay = int(1000 / fps)  # Delay between frames adjusted for video fps

last_toggle_time = time.time()  # Keep track of the last time the pause was toggled
debounce_time = 0.2  # 200 milliseconds debounce time

handler = ImageHandler()

# Specify the path to your MP4 file

# Check if the video was opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Read and display the video frame by frame
while True:
    if not pause:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # If frame is read correctly, ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Current timestamp in seconds

        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # Space bar to toggle pause
            current_time = time.time()
            if current_time - last_toggle_time >= debounce_time:
                pause = not pause
                last_toggle_time = current_time  # Update the last toggle time


        # Display the resulting frame
        sice, position, angle = handler.find_bench(frame)
        #angle_deg, center_x, done = handler.find_pipeline(frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC to exit
        break
    elif key == 32:  # Space bar to toggle pause
        current_time = time.time()
        if current_time - last_toggle_time >= debounce_time:
            pause = not pause
            last_toggle_time = current_time  # Update the last toggle time


# When everything done, release the video capture object and close all frames
cap.release()
cv2.destroyAllWindows()
