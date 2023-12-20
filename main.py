#Made by willmil11
#
#This uses micropython microbit environement that you can use by downloading
#uflash with pip, connecting the microbit to the computer and running uflash
#then flash this code to the microbit with uflash main.py. After that you can
#start playing.

from microbit import *
import random
from time import sleep as rsleep
import machine

godmode = False #Set to True for godmode (invincibility)
                #Set to False for normal mode (not invincibility)
                
cheatcodeCounter = 0

def sleep(ms):
    rsleep(ms / 1000)

player = {
    "x": 1,
    "y": 2
}

def randomId():
    return str(random.randint(0, 99999999))

useless = []

obstaclesNumber = 1
index = 0
obstacles = []

while True:
    display.clear()
    if index >= 85:
        #Reset to avoid memory explosion
        #Let's say player won to avoid confusion
        #Smiley with leds
        #00100
        #01010
        #00010
        #01010
        #00100
        display.clear()
        display.set_pixel(3, 0, 9)
        display.set_pixel(1, 1, 9)
        display.set_pixel(4, 1, 9)
        display.set_pixel(4, 2, 9)
        display.set_pixel(1, 3, 9)
        display.set_pixel(4, 3, 9)
        display.set_pixel(3, 4, 9)
        sleep(700)
        machine.reset()
    display.set_pixel(player["x"], player["y"], 9)

    # If index is a multiple of 30 add an obstacle
    if index % 100 == 0:
        obstaclesNumber += 1

    # Create an array of obstacles randomly placed between x = 3, 4, 5 and y = 0, 1, 2, 3, 4
    index2 = 0
    togen = obstaclesNumber - len(obstacles)
    while index2 < togen:
        x = random.randint(4, 5)
        y = random.randint(0, 4)
        #While pos is the same as a pos in obstacles regenerate
        index3 = 0
        while index3 < len(obstacles):
            #If exists
            try:
                obstacles[index3]
            except IndexError:
                index3 += 1
                continue
            else:
                pass

            try:
                obstacles[index3]["x"]
            except KeyError:
                index3 += 1
                continue
            else:
                pass
            
            try:
                obstacles[index3]["y"]
            except KeyError:
                index3 += 1
                continue
            else:
                pass

            if obstacles[index3]["x"] == x and obstacles[index3]["y"] == y:
                x = random.randint(4, 5)
                y = random.randint(0, 4)
                index3 = 0
            index3 += 1
        obstacles.append({"x": x, "y": y, "id": randomId()})
        index2 += 1

    # Move and remove obstacles
    index2 = 0
    while index2 < len(obstacles):
        obstacles[index2]["x"] -= 1
        index2 += 1
        #Add 1 to obstaclesNumber if the obstacle is off the screen and add it to useless to not add 1 to obstaclesNumber again
        #If not contained in useless
        if obstacles[index2 - 1]["x"] < 0 and obstacles[index2 - 1]["id"] not in useless:
            obstaclesNumber += 1
            useless.append(obstacles[index2 - 1]["id"])

    # Check if the player has hit an obstacle
    index2 = 0
    while index2 < obstaclesNumber:
        if godmode is True:
            break
        #If exists
        try:
            obstacles[index2]
        except IndexError:
            index2 += 1
            continue
        else:
            pass

        try:
            obstacles[index2]["x"]
        except KeyError:
            index2 += 1
            continue
        else:
            pass
        
        try:
            obstacles[index2]["y"]
        except KeyError:
            index2 += 1
            continue
        else:
            pass

        if obstacles[index2]["x"] == player["x"] and obstacles[index2]["y"] == player["y"]:
            #00001
            #01010
            #00010
            #01010
            #00001
            display.clear()
            display.set_pixel(4, 0, 9)
            display.set_pixel(1, 1, 9)
            display.set_pixel(3, 1, 9)
            display.set_pixel(3, 2, 9)
            display.set_pixel(1, 3, 9)
            display.set_pixel(3, 3, 9)
            display.set_pixel(4, 4, 9)
            sleep(700)
            machine.reset()
            index = 0
        index2 += 1

    # Draw the obstacles
    index2 = 0
    while index2 < obstaclesNumber:
        #If exists
        try: 
            obstacles[index2]
        except IndexError:
            index2 += 1
            continue
        else:
            pass

        try:
            obstacles[index2]["x"]
        except KeyError:
            index2 += 1
            continue
        else:
            pass
        
        try:
            obstacles[index2]["y"]
        except KeyError:
            index2 += 1
            continue
        else:
            pass

        if obstacles[index2]["x"] < 5 and obstacles[index2]["x"] > -1 and obstacles[index2]["y"] < 5 and obstacles[index2]["y"] > -1:
            display.set_pixel(obstacles[index2]["x"], obstacles[index2]["y"], 5)
        index2 += 1

    index += 1
    index2 = 0
    totaldelay = 200
    totalchunks = 50
    delay = totaldelay / totalchunks
    while index2 < totalchunks:
        # Move up with B
        # Move down with A
        ba = button_a.was_pressed()
        bb = button_b.was_pressed()
        if ba:
            player["y"] += 1
        if bb:
            player["y"] -= 1
        # If the player goes off the screen, make them wrap around
        if player["y"] > 4:
            player["y"] = 0
        if player["y"] < 0:
            player["y"] = 4
        if button_a.is_pressed() and button_b.is_pressed():
            cheatcodeCounter += 1
            if cheatcodeCounter >= 500:
                display.clear()
                display.set_pixel(1, 2, 9)
                display.set_pixel(2, 2, 9)
                display.set_pixel(3, 2, 9)
                sleep(700)
                
                #Set godmode to its invert
                godmode = not godmode
                cheatcodeCounter = 0
        index2 += 1
        sleep(delay)