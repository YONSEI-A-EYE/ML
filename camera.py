##if Raspberry :

import cv2

def get_stream_video():
    cam = cv2.VideoCapture(0)

    while True:
        success, image = cam.read()

        if not success:
            break
        else:
            success, buffer = cv2.imencode('.jpg', image)
            
            # transit + yield 
            image = buffer.tobytes() ## image -> byte
            yield (b'--image\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(image) + b'\r\n')