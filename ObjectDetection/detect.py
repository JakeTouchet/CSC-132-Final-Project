from ultralytics import YOLO
import cv2
import argparse
import time
from ultralytics.yolo.utils.plotting import Annotator

model = YOLO('yolov8n.pt')

def main(args):
    is_webcam = False
    is_video = False
    is_image = False

    # Decide if we are using webcam, video, or image file
    # Webcam
    if args.source == '0':
        is_webcam = True
        cap = cv2.VideoCapture(0) # Webcam from which to read the frames
        # Set the resolution of the webcam (done automatically?)
        # cap.set(3, 480)
        # cap.set(4, 480)
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
    

    prev_time = time.time()
    while True:
        time_elapsed = time.time() - prev_time

        if is_webcam or is_video:
            _, temp_frame = cap.read() # Temporarily store the frame from video (purges the buffer)

            if time_elapsed > 1./args.frame_rate: # Only process 1 frame every 1/args.frame_rate seconds
                prev_time = time.time() # Reset the timer

                frame = temp_frame # Use the frame from the buffer
                if args.im_show:
                    frame = annotate_frame(frame, res=res)
                    cv2.imshow('YOLO V8 Detection', frame)     

        else:
            # Image file
            if args.im_show:
                cv2.imshow('YOLO V8 Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        
def annotate_frame(frame, res = (640, 480)):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = model.predict(img)

    for r in results:
        
        annotator = Annotator(frame)
        
        boxes = r.boxes
        for box in boxes:
            
            b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
            c = box.cls
            mid_x = (b[2] - b[0])/2 + b[0]
            x_dist = res[0]/2 - mid_x
            annotator.box_label(b, model.names[int(c)] + f" {x_dist.item():.2f}")
            
    frame = annotator.result()
    return frame

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parameter Processing')

    parser.add_argument('--source', type=str, default='0', help='Source of the feed (0 for webcam, path to video file, path to image file)')
    parser.add_argument('--im_show', default=False, action=argparse.BooleanOptionalAction, help='Show the image feed (True/False))')
    parser.add_argument('--frame_rate', type=int, default=30, help='Frame rate of the feed (if webcam is used)')

    args = parser.parse_args()

    main(args)