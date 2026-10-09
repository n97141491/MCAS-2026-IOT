import RPi.GPIO as GPIO
import time

LED = 11
BUZZER = 13
freq = 523
unit = 0.2
short = unit
long = unit * 3

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(LED, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)
voice = GPIO.PWM(BUZZER, freq)

def signal(duration):
    GPIO.output(LED, GPIO.HIGH)
    voice.start(50)
    time.sleep(duration)
    GPIO.output(LED, GPIO.LOW)
    voice.stop()

def SOS():
    morse = ['...', '---', '...']
    letters = ['S', 'O', 'S']
    for i in range(len(morse)):
        print('Sending:', letters[i], morse[i])
        for j in range(len(morse[i])):
            signal(short if morse[i][j] == '.' else long)
            if j < len(morse[i]) - 1:
                time.sleep(unit)
        if i < len(morse) - 1:
            time.sleep(unit * 3)

try:
    print('Start SOS Morse Code')
    while True:
        SOS()
        print('SOS Complete')
        time.sleep(unit * 7)
except KeyboardInterrupt:
    print('\nProgram Stopped')
finally:
    voice.stop()
    GPIO.output(LED, GPIO.LOW)
    GPIO.cleanup()
