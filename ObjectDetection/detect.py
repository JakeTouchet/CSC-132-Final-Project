import sys
sys.path.append('..')

from ultralytics import YOLO
from RobotFiles.servo import *
import cv2
import argparse
import time
from ultralytics.yolo.utils.plotting import Annotator

model = YOLO('yolov8n.pt')

def main(args):
    # Use real gpio on rpi
    # Use fake gpio on anything else
    if is_raspberrypi():
        import RPi.GPIO as GPIO
    else:
        import fake_rpi
    GPIO = fake_rpi.fake_rpi.RPi.GPIO

    import time

    # Sets up output pins for communication with arduino
    bin_pin0 = 19
    bin_pin1 = 20
    bin_pin2 = 21
    bin_pin3 = 22

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(bin_pin0, GPIO.OUT)
    GPIO.setup(bin_pin1, GPIO.OUT)
    GPIO.setup(bin_pin2, GPIO.OUT)
    GPIO.setup(bin_pin3, GPIO.OUT)


    # Decide if we are using webcam, video, or image file
    is_webcam = False
    is_video = False
    is_image = False

    # Webcam
    if args.source == '0':
        is_webcam = True
        cap = cv2.VideoCapture(0) # Webcam from which to read the frames
        if not cap.isOpened():
            raise IOError("Couldn't open webcam or video")
        WIDTH, HEIGHT = int(cap.get(3)), int(cap.get(4))
        res = (WIDTH, HEIGHT) # Get resolution of the video
    # Video file
    elif args.source.endswith('.mp4') or args.source.endswith('.avi'):
        is_video = True
        print(args.source)
        cap = cv2.VideoCapture(args.source) # Video file from which to read the frames
        if not cap.isOpened():
            raise IOError("Couldn't open webcam or video")
        WIDTH, HEIGHT = int(cap.get(3)), int(cap.get(4))
        res = (WIDTH, HEIGHT) # Get resolution of the video
    # Image file
    elif args.source.endswith('.png') or args.source.endswith('.jpg'):
        is_image = True
        frame = cv2.imread(args.source) # Get frame from image file
        # Annotate image
        if args.im_show:
            frame = annotate_frame(frame)
    

    # Run inference
    prev_time = time.time()
    while True:
        time_elapsed = time.time() - prev_time

        if is_webcam or is_video:
            _, temp_frame = cap.read() # Temporarily store the frame from video (purges the buffer)

            if time_elapsed > 1./args.frame_rate: # Only process 1 frame every 1/args.frame_rate seconds
                prev_time = time.time() # Reset the timer

                frame = temp_frame # Use the frame from the buffer

                results = model.predict(frame)

                if args.im_show:
                    frame = annotate_frame(frame, results, res=res)
                    cv2.imshow('YOLO V8 Detection', frame)     
                
                # Get the distances from the center of the frame for specified classes
                x_dists = []
                for r in results:
                    if r.cls == args.cls:
                        boxes = r.boxes
                        for box in boxes:
                            b = box.xyxy[0]
                            x_dists += [get_distance(b, res=res)]
                
                # Get the closest object
                if len(x_dists) > 0:
                    x_dist = min(abs(x_dists))

                    # Turn robot to face object
                    if x_dist > 0:
                        timedTurn(x_dist)

        else:
            # Image file
            if args.im_show:
                cv2.imshow('YOLO V8 Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Recieves a box and gets distance from center of frame
def get_distance(box, res = (640, 480)):
    mid_x = (box[2] - box[0])/2 + box[0]
    x_dist = res[0]/2 - mid_x
    return x_dist

# Annotate with distance from center, class, and box
def annotate_frame(frame, results, res = (640, 480)):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    for r in results:
        
        annotator = Annotator(frame)
        
        boxes = r.boxes
        for box in boxes:
            
            b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
            c = box.cls
            x_dist = get_distance(b, res=res)
            annotator.box_label(b, model.names[int(c)] + f" {x_dist.item():.2f}")
            
    frame = annotator.result()
    return frame

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parameter Processing')

    parser.add_argument('--source', type=str, default='0', help='Source of the feed (0 for webcam, path to video file, path to image file)')
    parser.add_argument('--im_show', default=False, action=argparse.BooleanOptionalAction, help='Show the image feed (True/False))')
    parser.add_argument('--frame_rate', type=int, default=30, help='Frame rate of the feed (if webcam is used)')
    parser.add_argument('--cls', type=int, default=0, help='Class to track (0 for person, 1 for car, 2 for truck, 3 for bus, 4 for motorcycle, 5 for bicycle)')

    args = parser.parse_args()

    main(args)