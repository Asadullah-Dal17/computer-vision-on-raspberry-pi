
from picamera.array import PiRGBArray, raw_resolution
from picamera import PiCamera
import time
import cv2 as cv
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection

width, Height = 640, 480


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()

camera.resolution = (width, Height)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(width, Height))
# allow the camera to warmup

time.sleep(0.1)
with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as Detector:
    frame_counter =0
    start_time = time.time()

    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        frame_counter +=1
        image = frame.array

        image = cv.flip(image, 0) # flipping the image horizontaly cause my camera was up side down, "Appoglogies 😉"
        rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        height, width = image.shape[:2]
        result = Detector.process(rgb_image)
        if result.detections:
            for face in result.detections:
                x =int(face.location_data.relative_bounding_box.xmin *width)
                y = int(face.location_data.relative_bounding_box.ymin * height)
                w = int(face.location_data.relative_bounding_box.width *width)
                h = int(face.location_data.relative_bounding_box.height * height)
                cv.rectangle(image, (x, y), (x+w, y+h), (0,255,0), 2, cv.LINE_AA)
        # calculating the fps
        fps = frame_counter/(time.time() - start_time)
        cv.putText(image, f'FPS: {round(fps,2)}', (30,40), cv.FONT_HERSHEY_PLAIN, 1.3, (0,255,0),2)
        # show the frame
        cv.imshow("Frame", image)
        key = cv.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
