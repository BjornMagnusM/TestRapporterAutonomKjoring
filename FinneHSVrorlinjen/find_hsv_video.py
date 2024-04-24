import cv2
import numpy as np

def nothing(x):
    pass

video_path = 'Benk.mp4'  # Update this with the actual path to your video file
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Failed to load video from {video_path}")
    exit() 

cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 121, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 124, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 36, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 237, 255, nothing)

fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frames per second of the video
pause = False
delay = int(1000 / fps)  # Delay between frames adjusted for video fps

while True:
    if not pause:
        ret, frame = cap.read()
        if not ret:
            print("Reached end of video, rewinding...")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  # Current timestamp in seconds

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_range, upper_range)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Overlay time on the video
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(res, f"Time: {current_time:.2f}s", (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    stacked = np.hstack((frame, res))
    cv2.imshow('Trackbars', cv2.resize(stacked, None, fx=0.5, fy=0.5))

    key = cv2.waitKey(delay) & 0xFF
    if key == 27:
        break
    elif key == ord('s'):
        thearray = [[l_h, l_s, l_v], [u_h, u_s, u_v]]
        print(thearray)
        np.save('hsv_value', thearray)
    elif key == 32:
        pause = not pause

cap.release()
cv2.destroyAllWindows()
