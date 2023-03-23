import pygame
import servo as car

pygame.init()

canvas = pygame.display.set_mode((500,500))

pygame.display.set_caption("Input Receiver")
exit = False

speed = 3

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
            car.stop()
            car.shutdown()
            print("Exit")
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                print("K_UP", f"speed = {speed}")
                car.forward(speed)
            if event.key == pygame.K_DOWN:
                print("K_DOWN", f"speed = {speed}")
                car.backward(speed)
            if event.key == pygame.K_RIGHT:
                print("K_RIGHT", f"speed = {speed}")
                car.right(speed)
            if event.key == pygame.K_LEFT:
                print("K_LEFT", f"speed = {speed}")
                car.left(speed)
            
            if event.key == pygame.K_0:
                speed = 0
                print("K_0", f"speed = {speed}")
            if event.key == pygame.K_1:
                speed = 1
                print("K_1", f"speed = {speed}")
            if event.key == pygame.K_2:
                speed = 2
                print("K_2", f"speed = {speed}")                
            if event.key == pygame.K_3:
                speed = 3
                print("K_3", f"speed = {speed}")
                
        
        if event.type == pygame.KEYUP:
            car.stop()
            print("Stop")
    pygame.display.update()