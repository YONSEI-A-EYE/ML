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

counter = 0
ptime = 0
video_path = './video/a-eye_test.mp4'
#'./video/a-eye_test_before_fall.mp4'
#'./video/a-eye_test.mp4' -- (720, 1280)
#'./video/a-eye_test_2_before_fall.mp4'
#'./video/a-eye_test_2.mp4' -- (480, 272)
cap = cv2.VideoCapture(video_path)

# Read until video is completed // 비디오 읽는 부분
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
    ) as pose:
        while(cap.isOpened()):
            success, image = cap.read()
            if success == True:
                
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # Search for pose (탐지 start)
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
                    with open('./landmark/leftEar.txt', 'a') as f:
                        f.write(str(positions[counter][7]))
                        f.write("\n")

                    # Write Coordinates of right ear to file
                    with open('./landmark/rightEar.txt', 'a') as f:
                        f.write(str(positions[counter][8]))
                        f.write("\n")
                        counter+=1

                # Calculate FPS
                ctime = time.time()
                fps = int(1/(ctime-ptime))
                ptime = ctime

                # Time Logic
                time_passed = int((time.time() - start)*100)
                left_diff = 0
                
                # Trigger every 5 1/100 seconds
                if time_passed % 5 == 0:
                    if counter>0:
                        # Left Leg coordinate - left ear coordinate
                        left_diff = positions[counter-1][27][1] - positions[counter-1][7][1]
                        #right_diff = positions[counter-1][28][1] - positions[counter-1][8][1]
                        if left_diff>-60 and left_diff<60:
                            print(f"{left_diff} : 낙상감지!!")

                # result show
                cv2.imshow('A-EYE', image) #cv2.flip(image, 1)

                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break

            else: 
                break

cap.release()