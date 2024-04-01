import numpy as np
import cv2

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
chessboard_size = (7, 9)  # 7 corners in width, 6 in height
# Prepare object points based on the chessboard size
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

cap = cv2.VideoCapture(1)  # Just as an example, try 2, 3, 4, etc.

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if not ret:
        print("Failed to grab frame")
        break
    # Find the chess board corners
    ret2, corners = cv2.findChessboardCorners(gray, (7,9), None)
    # If found, add object points, image points (after refining them)
    if ret2 == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)
        # Draw and display the corners
        cv2.drawChessboardCorners(frame, (7,9), corners2, ret)
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    cv2.imshow('Video Feed', frame)  # Display the captured frame
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(mtx)
        print(dist)
        print(len(imgpoints))
        break


cap.release()  # Release the webcam
mean_error = 0
for i in range(len(objpoints)):
 imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
 error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
 mean_error += error
 
print( "total error: {}".format(mean_error/len(objpoints)) )
