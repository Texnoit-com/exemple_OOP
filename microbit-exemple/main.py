from microbit import *

# from .training import Running, SportsWalking, Swimming

x = 0
while True:
    
    if accelerometer.was_gesture('shake'):
        display.show(x)
        x += 1
    sleep(1000)
        