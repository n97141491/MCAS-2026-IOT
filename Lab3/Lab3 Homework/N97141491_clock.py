import time
from datetime import datetime
import tm1637

# Physical BOARD pin 23 = BCM GPIO11; BOARD pin 24 = BCM GPIO8.
# The common mcauser/micropython-style tm1637 Python library uses BCM numbers.
CLK_BCM = 11
DIO_BCM = 8

display = tm1637.TM1637(clk=CLK_BCM, dio=DIO_BCM)
display.brightness(3)

try:
    print('TM1637 clock started (Ctrl+C to stop)')
    last_second = None
    while True:
        now = datetime.now()
        if now.second != last_second:
            display.numbers(now.hour, now.minute, colon=(now.second % 2 == 0))
            print(f'{now:%H:%M:%S}  colon {"ON" if now.second % 2 == 0 else "OFF"}')
            last_second = now.second
        time.sleep(0.05)
except KeyboardInterrupt:
    print('\nClock stopped')
finally:
    display.write([0, 0, 0, 0])
