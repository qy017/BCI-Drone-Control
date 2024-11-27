import pygame
import time

pygame.init() #initialize pygame
pygame.joystick.init() #initialize pygame joystick


if pygame.joystick.get_count() == 0: # Check if any joystick is connected
    print("No controller detected.")
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Controller detected: {joystick.get_name()}")


try:   # Main loop to read joystick input
    while True:
        pygame.event.pump()  # Process events
        for i in range(joystick.get_numaxes()):
            axis = joystick.get_axis(i)
            #print(f"Axis {i} value: {axis}")
        
        for i in range(joystick.get_numbuttons()):
            
            button = joystick.get_button(i)
            if button == 1:
                match i:
                    case 0:
                        print("X Pressed")
                    case 1:
                        print("Circle Pressed")
                        
                    case 2:
                        print("Square Pressed")
                    case 3:
                        print("Triangle Pressed")
                    case 14:
                        print("arrow right Pressed")
                    case 13:
                        print("arrow left Pressed")
                    case 12:
                        print("arrow backward Pressed")
                    case 11:
                        print("arrow forward Pressed")
                    # case 4:
                    #     print("go up")
                    # case 16:
                    #     print("go down")
                button = 0
                time.sleep(.2)
            else:
                 print("idle")
            #print(f"Button {i} value: {button}")
except KeyboardInterrupt:
    print("Exiting...")



pygame.quit() #Quit pygame

