"""Lab 4-1: Read DHT11 temperature and humidity on Raspberry Pi.

Wiring (Raspberry Pi 40-pin header):
    DHT11 VCC  -> 3.3V (physical pin 1)
    DHT11 DATA -> GPIO4 / BCM4 (physical pin 7)
    DHT11 GND  -> GND (physical pin 6)
"""

import time

import adafruit_dht
import board


def main():
    dht_device = adafruit_dht.DHT11(board.D4)

    try:
        while True:
            try:
                temperature_c = dht_device.temperature
                humidity = dht_device.humidity

                if temperature_c is None or humidity is None:
                    print("Sensor reading unavailable. Try again.")
                else:
                    temperature_f = temperature_c * 9 / 5 + 32
                    print(
                        "Temp:{:.1f} C / {:.1f} F    Humidity: {}%".format(
                            temperature_c, temperature_f, humidity
                        ),
                        flush=True,
                    )
            except RuntimeError as err:
                # DHT11 readings can occasionally fail a checksum; retry next cycle.
                print(err, flush=True)

            time.sleep(2.0)
    except KeyboardInterrupt:
        print("\nStopped DHT11 monitoring.")
    finally:
        dht_device.exit()


if __name__ == "__main__":
    main()
