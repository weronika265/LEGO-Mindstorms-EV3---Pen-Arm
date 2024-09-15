#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

# ustawienie wymowy
ev3.speaker.set_speech_options('pl')

# inicjalizacja silników sterujących ramieniem
# silnik odpowiadający za ruch lewo, prawo ramienia
motor_neck = Motor(Port.B)
# silnik odpowiadający za ruch góra, dół ramienia
motor_arm = Motor(Port.C)

# inicjalizacja czujników
gyroSensor = GyroSensor(Port.S2)
colorSensor = ColorSensor(Port.S3)
touchSensor = TouchSensor(Port.S4)


def draw_dot_line():
    '''
    Funkcja wykonuje ruch ramieniem robota, rysując przerywaną linię.
    '''
    for _ in range(3):
        if touchSensor.pressed():
            break
        # obniż ramię do dołu
        motor_arm.run_angle(-20, 12)
        wait(1000)
        # przesuń ramię w lewą stronę (od strony kostki)
        motor_neck.run_angle(-10, 15)
        wait(1000)
        # podnieś ramię do góry
        motor_arm.run_angle(20, 10)
        wait(1000)
        # przesuń ramię w lewą stronę (od strony kostki)
        motor_neck.run_angle(-10, 15)
    # na sam koniec podnieś ramię wyżej do góry
    motor_arm.run_angle(30, 15)


def draw():
    '''
    Funkcja rysuje dzięki ruchom ramienia, którymi manipuluje się przez przyciski na kostce EV3 Brick.
    Przy wykryciu koloru czarnego, robot automatycznie zaczyna rysować przerywaną linię.
    '''
    # zmień kolor kostki na żółtą
    ev3.light.on(Color.YELLOW)
    while(not touchSensor.pressed()):
        # zmiana grafiki wyświetlanej na kostce
        ev3.screen.load_image(ImageFile.TARGET)
        if colorSensor.color() == Color.BLACK:
            ev3.speaker.say('rysuję przerywana linię')
            ev3.screen.load_image(ImageFile.LEFT)
            draw_dot_line()
            ev3.screen.clear()
            ev3.speaker.say('przechodzę w tryb manualny')
        print(gyroSensor.angle())
        # sterowanie ramieniem robota za pomocą przycisków na kostce, z ruchem przypisanym zgodnie z nazwami przycisków na kostce
        if Button.UP in ev3.buttons.pressed():
            motor_arm.run_angle(20, 5)
        elif Button.LEFT in ev3.buttons.pressed():
            motor_neck.run_angle(-40, 5)
        elif Button.RIGHT in ev3.buttons.pressed():
            motor_neck.run_angle(40, 5)
        elif Button.DOWN in ev3.buttons.pressed():
            motor_arm.run_angle(-20, 5)
        else:
            # przytrzymuj ramię w obecnej pozycji
            motor_arm.hold()
        wait(100)
    while colorSensor.color() == Color.BLACK:
        wait(10)
    
    while(gyroSensor.angle() is not 0):
        motor_neck.run_angle(50, 5)  
    draw_dot_line()

# Write your program here.
# porusz ramieniem na samym początku uruchomienia programu, wydaj dźwięk, przedstaw się
motor_arm.run_time(50, 300, wait=True)
ev3.speaker.beep()
ev3.speaker.say('dzien dobry, nazywam się pen arm')

# poczekaj z działaniem, dopóki nie naciśnięto czujnika dotyku
while(not touchSensor.pressed()):
    wait(10)

gyroSensor.reset_angle(0)

# motor_neck.run_until_stalled(100, then=Stop.COAST, duty_limit=50)
# MAX_RIGHT_ANGLE = gyroSensor.angle()
# motor_neck.run_until_stalled(-100, then=Stop.COAST, duty_limit=50)
# MAX_LIGHT_ANGLE = gyroSensor.angle()
# print(MAX_RIGHT_ANGLE, MAX_LIGHT_ANGLE)

ev3.light.on(Color.RED)
wait(1000)
draw()

# while(gyroSensor.angle() is not 0):
#     motor_neck.run(50)
