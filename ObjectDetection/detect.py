import sys
sys.path.append('..')

from ultralytics import YOLO
from RobotFiles.servo import *
import cv2
import argparse
import time
import threading
import queue
import pika
from ultralytics.yolo.utils.plotting import Annotator

model = YOLO('yolov8n.pt')
names = [name.lower() for name in model.names.values()]
print("Names: ", names)

running = False

def main(args):
    DEBUG = args.debug
    # Use real gpio on rpi
    # Use fake gpio on anything else
    if is_raspberrypi():
        import RPi.GPIO as GPIO
    else:
        import fake_rpi
        GPIO = fake_rpi.fake_rpi.RPi.GPIO

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

    TURN_THRESH = 0.2


    # Connect to RabbitMQ ########################################################
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='138.47.119.55', credentials=pika.PlainCredentials('admin1', 'admin1')))
    channel = connection.channel()

    channel.exchange_declare(exchange='GUI', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='GUI', queue=queue_name)

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True
        )

    # Asynchronously consume messages from RabbitMQ in daemon thread
    t = threading.Thread(target=channel.start_consuming)
    t.daemon = True
    t.start()
    ##############################################################################

    # Webcam
    if args.source == '0':
        cap = VideoCapture(0) # Webcam from which to read the frames
        WIDTH, HEIGHT = int(cap.cap.get(3)), int(cap.cap.get(4))
        res = (WIDTH, HEIGHT) # Get resolution of the video
        X_RES = int(res[0])
        Y_RES = int(res[1])
    
    for i in range(10):
        print(ultraDistance())

    global running

    # Run inference
    while True:
        current_frame = cap.read()

        print("loop")
        if current_frame is not None:
            if running:
                results = model.predict(current_frame)
                if DEBUG:
                    print(results)

                if args.im_show:
                    ann_frame = annotate_frame(current_frame, results, X_RES)
                    cv2.imshow('YOLO V8 Detection', ann_frame)
                
                # Get the distances from the center of the frame for specified classes
                x_dists = get_norm_distances(args, X_RES, results)
                
                # Get the closest object
                if len(x_dists) > 0:
                    min_dist = X_RES
                    for x_dist in x_dists:
                        if abs(x_dist) < abs(min_dist):
                            min_dist = x_dist

                    # Turn robot to face object
                    if abs(x_dist) > TURN_THRESH:
                        timedTurn(x_dist*2, speed=8)
                    else:
                        start_time = time.time()
                        moveUntil(0.5)
                        print("Stop: "+str(ultraDistance()))
                        running = False
                else:
                    timedTurn(5, speed=8)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

#TODO cite from stack overflow
class VideoCapture:
  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
        ret, frame = self.cap.read()
        if not ret:
            print("No frame")
            continue
        if not self.q.empty():
            try:
                self.q.get_nowait()   # discard previous (unprocessed) frame
            except queue.Empty:
                pass
        self.q.put(frame)

  def read(self):
    frame = None
    try:
        frame = self.q.get_nowait()
    except queue.Empty:
        pass
    return frame

# Callback function for RabbitMQ
def callback(ch, method, properties, body):
    global names
    global running

    body = body.decode()
    print(" [x] %r:%r" % (method.routing_key, body))

    # Process message
    if method.routing_key == 'class':
        args.cls = names.index(body.lower())
        print("Class set to " + str(args.cls))
    elif method.routing_key == 'control':
        if body == 'start':
            running = True
            print(running)
        elif body == 'stop':
            running = False
        elif body == 'off':
            exit()

# Get the normalized distances from the center of the frame for specified classes
def get_norm_distances(args, x_res, results):
    x_dists = []
    if len(results) > 0:
        for r in results:
            boxes = r.boxes
            for box in boxes:
                if box.cls == args.cls:
                    b = box.xyxy[0]
                    x_dists += [get_distance(b, x_res)/(x_res/2)]
    return x_dists

# Recieves a box and gets distance from center of frame
def get_distance(box, x_res):
    mid_x = (box[2] - box[0])/2 + box[0]
    x_dist = x_res/2 - mid_x
    return x_dist

# Annotate with distance from center, class, and box
def annotate_frame(frame, results, x_res):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    for r in results:
        annotator = Annotator(frame)
        
        boxes = r.boxes
        for box in boxes:
            
            b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
            c = box.cls
            x_dist = get_distance(b, x_res)/(x_res/2)
            annotator.box_label(b, model.names[int(c)] + f" {x_dist.item():.2f}")
            
    frame = annotator.result()
    return frame

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parameter Processing')

    parser.add_argument('--source', type=str, default='0', help='Source of the feed (0 for webcam, path to video file, path to image file)')
    parser.add_argument('--im_show', action='store_true', help='Show the image feed (True/False))')
    parser.add_argument('--cls', type=int, default=0, help='Class to track (0 for person, 1 for car, 2 for truck, 3 for bus, 4 for motorcycle, 5 for bicycle)')
    parser.add_argument('--debug', action='store_true', help='Debug mode (True/False)')

    args = parser.parse_args()

    main(args)