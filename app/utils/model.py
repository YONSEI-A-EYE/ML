import time
import cv2
from datetime import date, timedelta
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

time_passed = 0
start = time.time()
positions = [] #append (x,y) corrdinate to list
right_ear = [] 
left_ear = []
idx = 0
result = ''

video_path = '../video/a-eye_test.mp4'
#'./video/a-eye_test_before_fall.mp4'
#'./video/a-eye_test.mp4' -- (720, 1280)
#'./video/a-eye_test_2_before_fall.mp4'
#'./video/a-eye_test_2.mp4' -- (480, 272)

cam = cv2.VideoCapture(video_path)
# Read until video is completed
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
    ) as pose:
        while(cam.isOpened()):
            success, image = cam.read()
            if success == True:
                
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # Search for pose
                results = pose.process(image)
                if results.pose_landmarks:
                    mp_drawing.draw_landmarks( # Draw the pose annotation
                        image, 
                        results.pose_landmarks, 
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

                    # Convert results into array
                    lms = []

                    for id, lm in enumerate(results.pose_landmarks.landmark):
                        h, w, c = image.shape
                        cx, cy = int(lm.x*w), int(lm.y * h)
                        lms.append((cx, cy))
                    positions.append(lms)

                    # Write Coordinates of left ear to file
                    #right_ear.append(str(positions[idx][7]))
                    # with open('./landmark/leftEar.txt', 'a') as f:
                    #     f.write(str(positions[idx][7]))
                    #     f.write("\n")

                    # Write Coordinates of right ear to file
                    #left_ear.append(str(positions[idx][8]))
                    #with open('./landmark/rightEar.txt', 'a') as f:
                    #    f.write(str(positions[idx][8]))
                    #    f.write("\n")
                    idx+=1

                # Time
                time_passed = int((time.time() - start)*100)
                left_diff = 0
                
                # Trigger every 5 1/100 seconds
                if time_passed % 5 == 0:
                    if idx>0:
                        # Left Leg coordinate - left ear coordinate
                        left_diff = positions[idx-1][27][1] - positions[idx-1][7][1]
                        #right_diff = positions[idx-1][28][1] - positions[idx-1][8][1]
                        if left_diff>-60 and left_diff<60:
                            print(f"{left_diff} : DETECT BABY FALL!!")
                            break

                # result show
                cv2.imshow('A-EYE', image) #cv2.flip(image, 1)

                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break

            else: 
                break

cam.release()