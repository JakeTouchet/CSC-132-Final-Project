import pygame
import pika
import servo as car

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.1.3', credentials=pika.PlainCredentials('admin1', 'admin1')))
channel = connection.channel()
channel.exchange_declare(exchange='GUI', exchange_type='fanout')
channel.basic_publish(exchange='GUI', routing_key='', body='ServoControllerOn')


pygame.init()

canvas = pygame.display.set_mode((500,500))

pygame.display.set_caption("Input Receiver")
exit = False

speed = 8
lastDirection = []
direction = [0,0]
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 32)
speedModHeld = False

while not exit:
    clock.tick(60)

    keys = pygame.key.get_pressed()
    mods = pygame.key.get_mods()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            exit = True
            #car.stop()
            #car.shutdown()
            print("Exit")
        elif event.type == pygame.KEYUP and event.key in [pygame.K_MINUS, pygame.K_EQUALS, pygame.K_KP_PLUS, pygame.K_KP_MINUS]:
            speedModHeld = False
    
    lastDirection = direction
    direction = [0,0]
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        direction[0] += -1
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        direction[0] += 1
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        direction[1] += 1
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        direction[1] += -1
    
    
    if not speedModHeld:
        if mods & pygame.KMOD_SHIFT:
            if keys[pygame.K_EQUALS] or keys[pygame.K_KP_PLUS]:
                speed += 8
                speedModHeld = True
            elif keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
                speed -= 8
                speedModHeld = True
        else:
            if keys[pygame.K_EQUALS] or keys[pygame.K_KP_PLUS]:
                speed += 4
                speedModHeld = True
            elif keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
                speed -= 4
                speedModHeld = True

    speed = max(min(speed, 32),0)

    if direction != lastDirection:
        print(f"Act, {speed}, {direction}")
        if direction[0] > 0:
            #car.right(speed)
            channel.basic_publish(exchange='GUI', routing_key='manual', body=f'right {speed}')
        elif direction[0] < 0:
            #car.left(speed)
            channel.basic_publish(exchange='GUI', routing_key='manual', body=f'left {speed}')
        elif direction[1] > 0:
            #car.forward(speed)
            channel.basic_publish(exchange='GUI', routing_key='manual', body=f'forward {speed}')
        elif direction[1] < 0:
            #car.backward(speed)
            channel.basic_publish(exchange='GUI', routing_key='manual', body=f'backward {speed}')
        else:
            channel.basic_publish(exchange='GUI', routing_key='manual', body=f'stop {speed}')
            #car.stop()

    gui_speed = font.render(f"Speed = {speed}", True, (255,255,255))
    gui_direction = font.render(f"Direction = {'Forward' if direction[1] > 0 else 'Backward' if direction[1] < 0 else 'Right' if direction[0] > 0 else 'Left' if direction[0] < 0 else 'Stopped'}", True, (255,255,255))
    gui_US = font.render(f"Distance = {round(car.ultraDistance(), 5)}", True, (255,255,255))
    gui_IsTurning = font.render(f"Is Turning = {car.getIsTurning()}", True, (255,255,255))
    
    canvas.fill((0,0,0))
    canvas.blit(gui_speed, (0,0))
    canvas.blit(gui_direction, (0, gui_speed.get_height()))
    canvas.blit(gui_IsTurning, (0,gui_US.get_height()*2))
    canvas.blit(gui_US, (500-gui_US.get_width(),0))
    pygame.display.update()