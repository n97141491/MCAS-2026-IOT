import time
import RPi.GPIO as GPIO

TRIG_y = 23  # GPIO23, physical pin 16
ECHO_r = 24  # GPIO24, physical pin 18
WARNING_DISTANCE_CM = 20.0

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_y, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO_r, GPIO.IN)


def measure_distance():
    # HC-SR04 needs a trigger pulse of at least 10 microseconds.
    GPIO.output(TRIG_y, GPIO.LOW)
    time.sleep(0.0002)
    GPIO.output(TRIG_y, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_y, GPIO.LOW)

    deadline = time.monotonic() + 0.1
    while GPIO.input(ECHO_r) == GPIO.LOW:
        if time.monotonic() >= deadline:
            return None

    pulse_start = time.perf_counter()
    deadline = time.monotonic() + 0.1
    while GPIO.input(ECHO_r) == GPIO.HIGH:
        if time.monotonic() >= deadline:
            return None

    pulse_end = time.perf_counter()
    distance_cm = (pulse_end - pulse_start) * 34300 / 2
    if not 2 <= distance_cm <= 400:
        return None
    return distance_cm


try:
    print('程式啟動，按 Ctrl+C 可以停止測試...')
    while True:
        distance = measure_distance()
        if distance is None:
            print('測距失敗，正在重新測量...')
        else:
            print(f'目前距離: {distance:.2f} cm')
            if distance < WARNING_DISTANCE_CM:
                print('注意！！！')
            else:
                print('沒事')
        time.sleep(0.5)
except KeyboardInterrupt:
    print('\n停止測量中...')
finally:
    GPIO.cleanup()
    print('GPIO 已清理，程式結束。')
