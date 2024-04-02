import numpy as np
import cv2 


mtx = np.array(((426.17685011,   0,         320.38487224),
             (0,          429.76884458, 225.27715136),
             (0,           0,           1       ),))

dist = np.array(((-0.35653578,  0.11731714,  0.01052246,  0.00376304, -0.01392377),))
#Total error 0.28585107598100534



mtx2 = np.array(((422.65250774,   0,         339.39084058),
             (0,         415.93685696, 221.81006145),
             (0,           0,           1       ),))

dist2 = np.array(((-0.39301966,  0.19242641,  0.00989094, -0.00277074, -0.05723299),))


cap = cv2.VideoCapture(1)  # Just as an example, try 2, 3, 4, etc.


ret, frame = cap.read()

while True:
    ret, frame = cap.read()  # Read one frame from the webcam
    
    if not ret:
        print("Failed to grab frame")
        break
    img = frame.copy()
    h, w = frame.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]

    height = max(img.shape[0], dst.shape[0])
    width_img = int(img.shape[1] * (height / img.shape[0]))
    width_dst = int(dst.shape[1] * (height / dst.shape[0]))

    img_resized = cv2.resize(img, (width_img, height))
    dst_resized = cv2.resize(dst, (width_dst, height))
    
    imgshow = np.hstack((img_resized, dst_resized))
 
    cv2.imshow('Video Feed', imgshow)  # Display the captured frame
    
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Release the webcam
