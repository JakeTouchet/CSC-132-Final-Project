import servo as car
import pika
import argparse
import time
def main(args):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.1.3', credentials=pika.PlainCredentials('admin1', 'admin1')))
    channel = connection.channel()

    channel.exchange_declare(exchange='GUI', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange='GUI', queue=queue_name)

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True
            )
    
    while True:
        time.sleep(.1)
        channel.start_consuming()
# Callback function for RabbitMQ
def callback(ch, method, properties, body):
    global names
    global running

    body:str = body.decode()
    print(" [x] %r:%r" % (method.routing_key, body))

    # Process message
    if method.routing_key == 'manual':
        direction, speed = body.split()
        eval(f"car.{direction}({speed})")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parameter Processing')

    parser.add_argument('--source', type=str, default='0', help='Source of the feed (0 for webcam, path to video file, path to image file)')
    parser.add_argument('--im_show', action='store_true', help='Show the image feed (True/False))')
    parser.add_argument('--cls', type=int, default=0, help='Class to track (0 for person, 1 for car, 2 for truck, 3 for bus, 4 for motorcycle, 5 for bicycle)')
    parser.add_argument('--debug', action='store_true', help='Debug mode (True/False)')

    args = parser.parse_args()

    main(args)